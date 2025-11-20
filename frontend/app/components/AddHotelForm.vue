<template>
    <div class="container py-3">
        <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card shadow p-4">
            <h3 class="mb-4 fw-bold text-primary">新增飯店資訊</h3>

            <div v-if="!isOwner" class="alert alert-warning text-center">
                ⚠️ **權限不足：** 只有 **飯店業者 (Owner)** 才能新增飯店資訊。請登入或檢查權限。
            </div>

            <form @submit.prevent="addHotel" v-else>
                
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
import { ref ,computed, watch } from 'vue';
import { useAuthToken, useUser } from '~/composables/useAuth';

// 假設您的 API Base URL 是 http://127.0.0.1:8000
const API_URL = 'http://127.0.0.1:8000/hotels/create'; 

const loading = ref(false);
const errorMessage = ref('');
const successMessage = ref('');

//獲取使用者狀態(token)
const userState = useUser();
const authToken = useAuthToken();

// 🚩 檢查權限：確保已登入且角色為 'owner'
const isOwner = computed(() => {
    return !!authToken.value && userState.value && userState.value.role === 'owner' && userState.value.id;
});

// 🚩 表單數據：這裡不再包含 'owner' 欄位，保持乾淨
const hotelData = ref({
    hotel_name: '',
    location: '',
    room_type: '',
    price: null
});

// 處理表單提交的邏輯
const addHotel = async () => {
    // 1. 再次檢查權限
    if (!isOwner.value) {
        errorMessage.value = '您沒有權限執行此操作。';
        return;
    }

    errorMessage.value = '';
    successMessage.value = '';
    loading.value = true;

    // 2. 驗證價格是否為數字
    if (typeof hotelData.value.price !== 'number' || hotelData.value.price <= 0) {
        errorMessage.value = '請輸入有效的價格。';
        loading.value = false;
        return;
    }
    
    // 3. 準備 payload：只包含後端需要的這四個欄位
    // 🚨 這裡不包含 owner ID，因為後端會從 Header 的 Token 自動解析
    const payload = {
        hotel_name: hotelData.value.hotel_name,
        location: hotelData.value.location,
        room_type: hotelData.value.room_type,
        price: hotelData.value.price
    };

    // 4. 執行 API 請求 (POST)
    try {
        // 這裡不需要手動加 Header，因為您的 api-auth.js 會自動攔截並加入 Token
        const response = await $fetch(API_URL, {
            method: 'POST',
            body: payload, // 傳送乾淨的 payload
        });
        
        // 5. 請求成功
        successMessage.value = `飯店資訊新增成功！ID: ${response.hotel_id || response.id || 'N/A'}`;
        
        // 6. 清空表單
        hotelData.value = {
            hotel_name: '',
            location: '',
            room_type: '',
            price: null
        };
        
    } catch (error) {
        console.error('新增飯店失敗:', error);
        
        const apiDetail = error?.data?.detail 
        errorMessage.value = apiDetail 
            ? (typeof apiDetail === 'string' ? apiDetail : JSON.stringify(apiDetail))
            : '新增失敗，請檢查權限或資料格式。';
        
    } finally {
        loading.value = false;
    }
};

// 🚩 除錯：監聽 userState 變化並打印角色資訊
watch(userState, (newUser) => {
    if (newUser) {
        console.log('--- AddHotelForm 除錯資訊 ---');
        console.log('Token 存在:', !!authToken.value);
        console.log('當前用戶 ID:', newUser.id); 
        console.log('當前用戶角色:', newUser.role);
        console.log('是否為 Owner:', isOwner.value);
        console.log('------------------------------');
    }
}, { immediate: true });
</script>

<style scoped>
/* 簡單的樣式調整 */
.card {
  max-width: 600px;
  margin: auto;
}
</style>