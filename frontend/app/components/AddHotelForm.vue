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

                <button type="submit" class="btn btn-primary w-100" :disabled="loading">
                    <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
                    {{ loading ? '新增中...' : '確認新增' }}
                </button>
                <p v-if="msg" class="mt-3 text-center" :class="isError ? 'text-danger' : 'text-success'">
                    {{ msg }}
                </p>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
// 不需要再引入 useAuthToken 了
// import { useRuntimeConfig } from '#app';

// const config = useRuntimeConfig();
const apiBase = useApiUrl();
// 建議改用 config 設定的 API Base，比較彈性
const API_URL = `${apiBase}/hotels/create`;

const hotelData = ref({ hotel_name: '', location: '', room_type: '', price: null });
const msg = ref('');
const isError = ref(false);
const loading = ref(false);

const addHotel = async () => {
    msg.value = '';
    isError.value = false;
    loading.value = true;

    try {
        // 🚀 關鍵修改：
        // 1. 不需要讀取 Token
        // 2. 不需要手動加 Authorization Header
        // 3. 瀏覽器會自動把 HttpOnly Cookie 帶過去
        const response = await $fetch(API_URL, {
            method: 'POST',
            body: {
                hotel_name: hotelData.value.hotel_name,
                location: hotelData.value.location,
                room_type: hotelData.value.room_type,
                price: hotelData.value.price
            },
            // 如果遇到跨域問題 (localhost:3000 -> 127.0.0.1:8000)，可能需要加這行：
            credentials: 'include' 
        });
        
        msg.value = `✅ 成功！飯店 ID: ${response.hotel_id || response.id}`;
        // 清空表單
        hotelData.value = { hotel_name: '', location: '', room_type: '', price: null };
        
    } catch (error) {
        console.error('API 錯誤:', error);
        isError.value = true;
        
        if (error.response?.status === 401) {
            msg.value = '❌ 權限不足：請先登入 (Cookie 失效)';
        } else {
            msg.value = `❌ 錯誤: ${error.data?.detail || error.message}`;
        }
    } finally {
        loading.value = false;
    }
};
</script>