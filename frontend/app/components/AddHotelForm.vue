<template>
  <div class="container">
    <div class="card shadow border-0 rounded-4 overflow-hidden mx-auto" style="max-width: 800px;">
      
      <div class="card-header bg-primary p-1"></div>

      <div class="card-body p-4 p-md-5">
        
        <div class="d-flex align-items-center mb-4">
          <div class="bg-primary bg-opacity-10 p-3 rounded-circle me-3">
            <i class="bi bi-building-add text-primary fs-4"></i>
          </div>
          <div>
            <h4 class="fw-bold mb-1">新增房間資訊</h4>
            <p class="text-muted mb-0 small">請填寫詳細資訊以建立新的住宿選項。</p>
          </div>
        </div>

        <form @submit.prevent="handleSubmit">
          <div class="row g-4">
            
            <div class="col-12">
              <label class="form-label fw-bold text-secondary small">飯店名稱</label>
              <div class="input-group input-group-lg">
                <span class="input-group-text bg-light border-end-0 text-muted">
                  <i class="bi bi-card-heading"></i>
                </span>
                <input 
                  v-model="hotelData.hotel_name" 
                  type="text" 
                  class="form-control bg-light ps-1" 
                  placeholder="例如：信義神氣大飯店" 
                  required
                />
              </div>
            </div>

            <div class="col-md-6">
              <label class="form-label fw-bold text-secondary small">地點</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0 text-muted">
                  <i class="bi bi-geo-alt-fill"></i>
                </span>
                <input 
                  v-model="hotelData.location" 
                  type="text" 
                  class="form-control bg-light ps-1" 
                  placeholder="城市或區域" 
                  required
                />
              </div>
            </div>

            <div class="col-md-6">
              <label class="form-label fw-bold text-secondary small">每晚價格 (TWD)</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0 text-muted fw-bold">
                  $
                </span>
                <input 
                  v-model="hotelData.price" 
                  type="number" 
                  class="form-control bg-light ps-1" 
                  placeholder="0"
                  min="1" 
                  required
                />
              </div>
            </div>

             <div class="col-12">
              <label class="form-label fw-bold text-secondary small">房型</label>
              <div class="input-group">
                <span class="input-group-text bg-light border-end-0 text-muted">
                  <i class="bi bi-houses-fill"></i>
                </span>
                <select v-model="hotelData.room_type" class="form-select bg-light ps-1" required>
                  <option value="" disabled selected>請選擇適用房型</option>
                  <option value="單人房">👤 單人房 (Single Room)</option>
                  <option value="雙人房">👥 雙人房 (Double Room)</option>
                  <option value="四人房">👨‍👩‍👧‍👦 四人房 (Quad Room)</option>
                  <option value="豪華套房">✨ 豪華套房 (Deluxe Suite)</option>
                  <option value="家庭房">🏡 家庭房 (Family Room)</option>
                  <option value="總統套房">👑 總統套房 (Presidential Suite)</option>
                </select>
              </div>
            </div>

          </div> <hr class="my-4 text-muted opacity-25">

          <button 
            type="submit" 
            class="btn btn-primary w-100 py-3 fw-bold d-flex align-items-center justify-content-center btn-hover-effect"
            :disabled="isSubmitting"
          >
            <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="bi bi-check-circle-fill me-2 fs-5"></i>
            {{ isSubmitting ? '正在建立中...' : '確認新增房源' }}
          </button>

        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue';
import Swal from 'sweetalert2';

// const config = useRuntimeConfig();
const apiBase = useApiUrl()

// 定義資料結構
const hotelData = reactive({
  hotel_name: '',
  location: '',
  room_type: '',
  price: ''
});

const isSubmitting = ref(false);

const handleSubmit = async () => {
  isSubmitting.value = true;
  
  // 模擬一個延遲，讓使用者看到 loading 狀態，感覺更專業
  await new Promise(resolve => setTimeout(resolve, 800));

  try {
    const response = await $fetch(`${apiBase}/hotels/create`, {
      method: 'POST',
      body: { ...hotelData, price: Number(hotelData.price) }, // 確保價格是數字
      credentials: 'include'
    });

    Swal.fire({
      icon: 'success',
      title: '新增成功！',
      text: `${hotelData.hotel_name} 已成功建立。`,
      confirmButtonColor: '#0d6efd',
      timer: 2000
    });

    // 清空表單
    Object.assign(hotelData, {
      hotel_name: '',
      location: '',
      room_type: '',
      price: ''
    });

  } catch (error) {
    Swal.fire({
      icon: 'error',
      title: '新增失敗',
      text: error.data?.detail || '系統發生錯誤，請稍後再試。',
      confirmButtonColor: '#dc3545'
    });
  } finally {
    isSubmitting.value = false;
  }
};
</script>

<style scoped>
/* 讓輸入框聚焦時，邊框顏色更柔和，並移除預設的強烈陰影 */
.form-control:focus, .form-select:focus {
  border-color: #86b7fe;
  box-shadow: 0 0 0 0.25rem rgba(13, 110, 253, 0.15);
  background-color: #fff !important; /* 聚焦時變回純白背景 */
}

/* 調整 Input Group 圖示的背景和邊框，讓它看起來跟輸入框是一體的 */
.input-group-text {
  border-color: #dee2e6;
}
.form-control, .form-select {
  border-color: #dee2e6;
}

/* 按鈕懸停微互動效果 */
.btn-hover-effect {
  transition: all 0.3s ease;
}
.btn-hover-effect:hover:not(:disabled) {
  transform: translateY(-2px); /* 微微上浮 */
  box-shadow: 0 .5rem 1rem rgba(13, 110, 253, 0.25) !important; /* 增加陰影 */
}
</style>