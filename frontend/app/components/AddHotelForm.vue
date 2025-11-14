<template>
    <div class="add-hotel-form-wrapper">
        <div class="row justify-content-center">
            <div class="col-md-12"> <div class="card shadow p-4">
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
const API_URL = 'http://127.0.0.1:8000/create_hotel/'; 

const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

// 🚩 表單數據的響應式狀態
const hotelData = ref({
    hotel_name: '',
    location: '',
    room_type: '',
    price: null,
});

// 處理表單提交的邏輯
const addHotel = async () => {
    errorMessage.value = '';
    successMessage.value = '';
    loading.value = true;

    if (typeof hotelData.value.price !== 'number' || hotelData.value.price <= 0) {
        errorMessage.value = '請輸入有效的價格。';
        loading.value = false;
        return;
    }
    
    try {
        const response = await $fetch(API_URL, {
            method: 'POST',
            body: hotelData.value,
        });
        
        successMessage.value = `飯店資訊新增成功！ID: ${response.id || 'N/A'}`;
        
        // 清空表單
        hotelData.value = {
            hotel_name: '',
            location: '',
            room_type: '',
            price: null,
        };
        
    } catch (error) {
        console.error('新增飯店失敗:', error);
        errorMessage.value = error?.data?.detail || '新增失敗，請檢查 API 連線與資料格式。';
        
    } finally {
        loading.value = false;
    }
};
</script>

<style scoped>
/* 簡單的樣式調整 */
/* 這裡的 card max-width 應由父組件的 col-lg-8 處理，但保留以防萬一 */
.card {
  /* max-width: 600px;  */
  margin: auto;
}
</style>