<template>
  <div class="container py-5">
    <div class="d-flex justify-content-between align-items-center mb-4">
      <h2 class="text-primary fw-bold">
        <i class="bi bi-building-gear me-2"></i>管理我的飯店
      </h2>
      <button class="btn btn-outline-primary" @click="refreshHotels">
        <i class="bi bi-arrow-clockwise"></i> 重新整理
      </button>
    </div>

    <div v-if="pending" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-2 text-muted">正在載入您的飯店資料...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger text-center">
      <i class="bi bi-exclamation-triangle-fill me-2"></i>
      載入失敗：{{ error.data?.detail || '無法連線到伺服器' }}
    </div>

    <div v-else>
      <div v-if="hotels && hotels.length > 0" class="card shadow-sm">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead class="table-light">
              <tr>
                <th scope="col" class="py-3 ps-4">#ID</th>
                <th scope="col" class="py-3">飯店名稱</th>
                <th scope="col" class="py-3">地點</th>
                <th scope="col" class="py-3">房型</th>
                <th scope="col" class="py-3">價格</th>
                <th scope="col" class="py-3 text-center">操作</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="hotel in hotels" :key="hotel.id">
                <td class="ps-4 fw-bold text-secondary">#{{ hotel.id }}</td>
                <td>
                  <NuxtLink 
                    :to="`/rooms/${hotel.id}`" 
                    class="fw-bold text-primary text-decoration-none hover-underline d-inline-flex align-items-center"
                    target="_blank" 
                  >
                    <span>{{ hotel.hotel_name }}</span>
                    <i class="bi bi-box-arrow-up-right small ms-2" style="font-size: 0.8em; transform: translateY(-1px);"></i>
                    </NuxtLink>
                </td>
                <td><i class="bi bi-geo-alt-fill text-danger me-1"></i>{{ hotel.location }}</td>
                <td><span class="badge bg-info text-dark">{{ hotel.room_type }}</span></td>
                <td class="fw-bold text-success">${{ hotel.price.toLocaleString() }}</td>
                <td class="text-center">
                  <button 
                    class="btn btn-outline-danger btn-sm" 
                    @click="deleteHotel(hotel.id, hotel.hotel_name)"
                    :disabled="isDeleting"
                  >
                    <i class="bi bi-trash3-fill me-1"></i> 刪除
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div v-else class="text-center py-5 bg-light rounded border border-dashed">
        <i class="bi bi-house-slash display-4 text-muted"></i>
        <h4 class="mt-3 text-muted">您還沒有新增任何飯店</h4>
        <p>趕快去「新增飯店」頁籤建立您的第一間飯店吧！</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import Swal from 'sweetalert2';

const config = useRuntimeConfig();
const isDeleting = ref(false);

// 1. 獲取飯店列表 (GET /hotels/my_hotels)
const { data: responseData, pending, error, refresh: refreshHotels } = await useFetch(
  `${config.public.apiBase}/hotels/my_hotels`,
  {
    // 🚀 關鍵修改 A: 
    // 1. server: false -> 強制在瀏覽器執行，避開 Docker 內部網路問題
    // 2. credentials: 'include' -> 確保帶上 HttpOnly Cookie
    server: false,
    credentials: 'include'
  }
);

const hotels = computed(() => {
  return responseData.value?.hotels || [];
});

// 3. 刪除邏輯
const deleteHotel = async (id, name) => {
  const result = await Swal.fire({
    title: '確定要刪除嗎？',
    html: `您即將刪除飯店：<b class="text-danger">${name}</b><br>此操作無法復原！`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc3545',
    cancelButtonColor: '#6c757d',
    confirmButtonText: '是的，狠心刪除',
    cancelButtonText: '取消'
  });

  if (!result.isConfirmed) return;

  isDeleting.value = true;
  try {
    // 🚀 關鍵修改 B: 加上 credentials: 'include'
    await $fetch(`${config.public.apiBase}/hotels/delete/${id}`, {
      method: 'DELETE',
      credentials: 'include' 
    });

    await Swal.fire({
      icon: 'success',
      title: '刪除成功',
      text: '該飯店資訊已移除',
      timer: 1500,
      showConfirmButton: false
    });
    
    refreshHotels();

  } catch (err) {
    console.error(err);
    Swal.fire({
      icon: 'error',
      title: '刪除失敗',
      text: err.data?.detail || '系統發生錯誤，請稍後再試'
    });
  } finally {
    isDeleting.value = false;
  }
};
</script>

<style scoped>
/* 原有的樣式保留 */
.table-hover tbody tr:hover {
  background-color: #f8f9fa;
  transition: background-color 0.2s;
}
.border-dashed {
    border-style: dashed !important;
}

/* 新增：滑鼠移過連結時顯示底線 */
.hover-underline:hover {
    text-decoration: underline !important;
}
</style>