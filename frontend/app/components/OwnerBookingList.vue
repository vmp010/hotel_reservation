<template>
  <div class="card shadow-sm">
    <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center">
      <h5 class="mb-0 fw-bold text-primary">
        <i class="bi bi-calendar-check me-2"></i>房客預訂清單
        
        <span v-if="pending && bookings" class="ms-2 badge bg-light text-secondary fw-normal">
            <span class="spinner-border spinner-border-sm me-1" role="status"></span>
            更新中...
        </span>
      </h5>
      
      <button class="btn btn-sm btn-outline-secondary" @click="refresh">
        <i class="bi bi-arrow-clockwise"></i> 刷新
      </button>
    </div>

    <div class="card-body p-0">
      
      <div v-if="pending && !bookings" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-2 text-muted">正在載入訂單資料...</p>
      </div>

      <div v-else-if="error" class="alert alert-danger m-3">
        載入失敗：{{ error.message }}
      </div>

      <div v-else-if="bookings && bookings.length > 0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0" :class="{ 'opacity-50': pending }">
            <thead class="table-light">
              <tr>
                <th scope="col" class="ps-4">#編號</th>
                <th scope="col">預訂飯店 / 房型</th>
                <th scope="col">房客資訊</th>
                <th scope="col">入住 / 退房日期</th>
                <th scope="col">狀態</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in paginatedBookings" :key="item.booking_id">
                <td class="ps-4 fw-bold text-secondary">#{{ item.booking_id }}</td>
                <td>
                  <div class="fw-bold">{{ item.hotel_name }}</div>
                  <small class="text-muted">{{ item.room_type }}</small>
                </td>
                <td>
                  <div><i class="bi bi-person-fill me-1"></i>{{ item.guest_name }}</div>
                  <small class="text-muted text-break">{{ item.guest_email }}</small>
                </td>
                <td>
                  <div class="text-success"><i class="bi bi-box-arrow-in-right me-1"></i>{{ item.check_in }}</div>
                  <div class="text-danger"><i class="bi bi-box-arrow-right me-1"></i>{{ item.check_out }}</div>
                </td>
                <td>
                  <span v-if="item.is_active" class="badge bg-success rounded-pill">已付款</span>
                  <span v-else class="badge bg-secondary rounded-pill">已取消</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div v-if="bookings.length > itemsPerPage" class="d-flex justify-content-between align-items-center p-3 border-top bg-light">
            <span class="text-muted small">
                顯示第 {{ startIndex + 1 }} 到 {{ Math.min(endIndex, filteredBookings.length) }} 筆，共 {{ filteredBookings.length }} 筆
            </span>
            
            <nav aria-label="Page navigation">
                <ul class="pagination pagination-sm mb-0">
                    <li class="page-item" :class="{ disabled: currentPage === 1 }">
                        <button class="page-link" @click="currentPage--">
                            <i class="bi bi-chevron-left"></i>
                        </button>
                    </li>
                    
                    <li class="page-item disabled">
                        <span class="page-link text-dark">
                            {{ currentPage }} / {{ totalPages }}
                        </span>
                    </li>

                    <li class="page-item" :class="{ disabled: currentPage === totalPages }">
                        <button class="page-link" @click="currentPage++">
                            <i class="bi bi-chevron-right"></i>
                        </button>
                    </li>
                </ul>
            </nav>
        </div>

      </div>

      <div v-else class="text-center py-5 text-muted">
        <i class="bi bi-inbox display-4"></i>
        <p class="mt-3">目前沒有任何預訂資料</p>
      </div>
    </div>
  </div>
</template>

<script setup>
// ❌ 移除 useAuthToken (因為 HttpOnly Cookie 前端讀不到)
// import { useAuthToken } from '~/composables/useAuth'; 
import { ref, computed, onMounted, onUnmounted } from 'vue';

// const config = useRuntimeConfig();
const apiBase = useApiUrl();
// ❌ 移除這行
// const authToken = useAuthToken(); 

let timer = null;

// --- 分頁設定 ---
const currentPage = ref(1); 
const itemsPerPage = 4;    

// API 請求
const { data: bookings, pending, error, refresh } = await useFetch(
  `${apiBase}/bookings/owner/all`,
  {
    // 🚀 關鍵修改 1: 移除 headers
    // headers: { 'Authorization': `Bearer ${authToken.value}` }, <--- 刪除這行

    // 🚀 關鍵修改 2: 加上 server: false
    // 因為在 Docker 內 Server 端抓不到 localhost，且 Cookie 在 SSR 傳遞較麻煩
    // 直接讓瀏覽器端 (Client) 去抓，瀏覽器會自動把 HttpOnly Cookie 帶給後端
    server: false,
    credentials: 'include'
    
    // immediate: !!authToken.value <--- 刪除這行，預設就是 true
  }
);

// --- 前端過濾邏輯 (只顯示 PAID) ---
const filteredBookings = computed(() => {
    if (!bookings.value) return [];
    // 這裡維持您原本的邏輯
    return bookings.value.filter(item => item.status && item.status.toUpperCase() === 'PAID');
});

// --- 分頁邏輯 (維持不變) ---
const totalPages = computed(() => {
    if (filteredBookings.value.length === 0) return 1;
    return Math.ceil(filteredBookings.value.length / itemsPerPage);
});

const startIndex = computed(() => {
    return (currentPage.value - 1) * itemsPerPage;
});

const endIndex = computed(() => {
    return startIndex.value + itemsPerPage;
});

const paginatedBookings = computed(() => {
    return filteredBookings.value.slice(startIndex.value, endIndex.value);
});

// --- 自動刷新 ---
onMounted(() => {
    timer = setInterval(() => {
        refresh(); 
    }, 5000);
});

onUnmounted(() => {
    if (timer) clearInterval(timer);
});
</script>

<style scoped>
.table {
    transition: opacity 0.3s ease;
}
/* 讓分頁按鈕好按一點 */
.page-link {
    cursor: pointer;
}
</style>