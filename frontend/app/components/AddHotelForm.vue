<template>
    <floder/>
    <div class="container py-5">
        <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow p-4">
            <h3 class="mb-4 fw-bold text-primary">新增飯店資訊</h3>

            <form @submit.prevent="addHotel">
                
                <div class="mb-3">
                <label for="hotelName" class="form-label">飯店名稱</label>
                <input
                    v-model="hotelData.hotel_name"
                    type="text"
                    class="form-control"
                    id="hotelName"
                    placeholder="例如：台北豪華飯店"
                    required
                />
                </div>

                <div class="mb-3">
                <label for="location" class="form-label">地點/地址</label>
                <input
                    v-model="hotelData.location"
                    type="text"
                    class="form-control"
                    id="location"
                    placeholder="例如：台北市信義區"
                    required
                />
                </div>

                <div class="mb-3">
                <label for="roomType" class="form-label">房型</label>
                <input
                    v-model="hotelData.room_type"
                    type="text"
                    class="form-control"
                    id="roomType"
                    placeholder="例如：豪華雙人房"
                    required
                />
                </div>

                <div class="mb-3">
                <label for="price" class="form-label">價格 (每晚)</label>
                <input
                    v-model.number="hotelData.price"
                    type="number"
                    class="form-control"
                    id="price"
                    placeholder="例如：3200"
                    min="0"
                    required
                />
                </div>

                <div class="d-grid mt-4">
                <button type="submit" class="btn btn-primary" :disabled="loading">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2" role="status"></span>
                    {{ loading ? '新增中...' : '確認新增飯店' }}
                </button>
                </div>

                <p v-if="successMessage" class="text-success mt-3 text-center fw-bold">{{ successMessage }}</p>
                <p v-if="errorMessage" class="text-danger mt-3 text-center">{{ errorMessage }}</p>

            </form>
            </div>
        </div>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

// 假設您的 API Base URL 是 http://127.0.0.1:8000
const API_URL = 'http://127.0.0.1:8000/create_hotel/'; // 假設 POST 端點是 /hotels/

const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

// 🚩 表單數據的響應式狀態，結構需與 API 要求的 JSON 體一致
const hotelData = ref({
  hotel_name: '',
  location: '',
  room_type: '',
  price: null, // 使用 null 或 0 作為初始數值
});

// 處理表單提交的邏輯
const addHotel = async () => {
  // 1. 重設訊息和狀態
  errorMessage.value = '';
  successMessage.value = '';
  loading.value = true;

  // 2. 驗證價格是否為數字
  if (typeof hotelData.value.price !== 'number' || hotelData.value.price <= 0) {
    errorMessage.value = '請輸入有效的價格。';
    loading.value = false;
    return;
  }
  
  // 3. 執行 API 請求 (POST)
  try {
    const response = await $fetch(API_URL, {
      method: 'POST',
      body: hotelData.value, // 直接將響應式對象作為 JSON 體發送
      // 🚩 注意：如果您的 API 需要驗證 (例如 Bearer Token)，您需要在 headers 中添加
      // headers: {
      //   'Authorization': `Bearer ${您的Token}` 
      // }
    });
    
    // 4. 請求成功
    successMessage.value = `飯店資訊新增成功！ID: ${response.id || 'N/A'}`;
    
    // 5. 清空表單
    hotelData.value = {
      hotel_name: '',
      location: '',
      room_type: '',
      price: null,
    };
    
  } catch (error) {
    // 6. 請求失敗或 API 返回錯誤
    console.error('新增飯店失敗:', error);
    // 嘗試從錯誤響應中獲取詳細訊息
    errorMessage.value = error?.data?.detail || '新增失敗，請檢查 API 連線與資料格式。';
    
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
/* 簡單的樣式調整 */
.card {
  max-width: 600px;
  margin: auto;
}
</style>