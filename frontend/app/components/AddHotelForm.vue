<template>
    <div class="container py-3">
        <div class="card shadow p-4" style="max-width: 600px; margin: auto;">
            <h3 class="mb-4 fw-bold text-primary">新增飯店</h3>
            
            <form @submit.prevent="addHotel">
                <div class="mb-3">
                    <label class="form-label">飯店名稱</label>
                    <input v-model="hotelData.hotel_name" type="text" class="form-control" placeholder="神奇大飯店" required />
                </div>
                <div class="mb-3">
                    <label class="form-label">地點</label>
                    <input v-model="hotelData.location" type="text" class="form-control" placeholder="台北市信義區" required />
                </div>

                <div class="mb-3">
                    <label class="form-label">房型</label>
                    <select v-model="hotelData.room_type" class="form-select" required>
                        <option value="" disabled>請選擇房型</option>
                        <option value="單人房">單人房 (Single Room)</option>
                        <option value="雙人房">雙人房 (Double Room)</option>
                        <option value="四人房">四人房 (Quad Room)</option>
                        <option value="豪華套房">豪華套房 (Deluxe Suite)</option>
                        <option value="家庭房">家庭房 (Family Room)</option>
                        <option value="總統套房">總統套房 (Presidential Suite)</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label">價格</label>
                    <input v-model.number="hotelData.price" type="number" class="form-control" placeholder="2000" required />
                </div>

                <button type="submit" class="btn btn-primary w-100">確認新增</button>
                <p v-if="msg" class="mt-3 text-center" :class="isError ? 'text-danger' : 'text-success'">
                    {{ msg }}
                </p>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import { useAuthToken } from '~/composables/useAuth';

// 🚨 統一用 localhost，不要用 127.0.0.1
const API_URL = 'http://localhost:8000/hotels/create'; 

const hotelData = ref({ hotel_name: '', location: '', room_type: '', price: null });
const msg = ref('');
const isError = ref(false);

// 取得 Token
const authToken = useAuthToken();

// 顯示 Token 長度用來除錯
const tokenLength = computed(() => authToken.value ? authToken.value.length : '無 Token');

const addHotel = async () => {
    msg.value = '傳送中...';
    isError.value = false;

    // 1. 優先從 Cookie 拿，如果沒有就從 LocalStorage 拿 (雙重保險)
    let token = authToken.value;
    if (!token && process.client) {
        token = localStorage.getItem('manual_token');
    }

    if (!token) {
        msg.value = '❌ 錯誤：找不到 Token，請重新登入';
        isError.value = true;
        return;
    }

    try {
        console.log('準備發送請求，Token:', token.substring(0, 10) + '...');

        // 2. 🚨 關鍵：手動加入 Header，不依賴攔截器
        const response = await $fetch(API_URL, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`, // 手動拼接
                'Content-Type': 'application/json'
            },
            body: {
                hotel_name: hotelData.value.hotel_name,
                location: hotelData.value.location,
                room_type: hotelData.value.room_type,
                price: hotelData.value.price
            }
        });
        
        msg.value = `✅ 成功！飯店 ID: ${response.hotel_id || response.id}`;
        // 清空表單
        hotelData.value = { hotel_name: '', location: '', room_type: '', price: null };
        
    } catch (error) {
        console.error('API 錯誤:', error);
        isError.value = true;
        
        if (error.status === 401) {
            msg.value = '❌ 401 Unauthorized：後端拒絕了 Token。';
        } else {
            msg.value = `❌ 錯誤 (${error.status}): ${error.data?.detail || error.message}`;
        }
    }
};
</script>