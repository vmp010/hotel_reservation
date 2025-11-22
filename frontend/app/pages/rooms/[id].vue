<template>
  <div class="container py-5">
    <NuxtLink to="/homeView" class="btn btn-secondary mt-3">
      <i class="bi bi-arrow-left"></i> 返回
    </NuxtLink>

    <div v-if="pending" class="text-center py-5 text-muted">
      <div class="spinner-border text-primary mb-2" role="status"></div>
      <p>資料載入中...</p>
    </div>

    <div v-else-if="room">
      <h1 class="mt-4">{{ room.hotel_name }}</h1>
      
      <div class="card shadow-sm p-4 mt-3">
        <p class="fs-5">🏠 飯店名稱：<strong>{{ room.hotel_name }}</strong></p>
        <p class="fs-5">📍 地點：{{ room.location }}</p>
        <p class="fs-5">💰 價格：<span class="text-danger fw-bold">${{ room.price }}</span> / 晚</p>
        <p class="fs-5">🛏️ 房型：{{ room.room_type }}</p>

        <div class="mt-4">
            <button 
                class="btn btn-warning btn-lg w-100 fw-bold text-dark" 
                @click="addToCart"
                :disabled="isBooking"
            >
                <span v-if="isBooking" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="bi bi-bag-plus-fill me-2"></i> 
                {{ isBooking ? '處理中...' : '加入購物車 / 預定' }}
            </button>
        </div>
      </div>
    </div>

    <div v-else class="text-center text-muted py-5">
      <h3>查無此房型 😅</h3>
      <NuxtLink to="/homeView" class="btn btn-primary mt-3">回首頁</NuxtLink>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Swal from 'sweetalert2'; // 引入 SweetAlert2
import { useAuthToken, useUser } from '~/composables/useAuth'; // 引入 Token 管理

const route = useRoute();
const router = useRouter();
const config = useRuntimeConfig();

// 取得 Token 與 User 狀態
const authToken = useAuthToken();
const user = useUser();

const isBooking = ref(false); // 控制按鈕 loading 狀態

// 1. 獲取房間詳細資料
// 🚨 修正：原本的 watch 是多餘的，useFetch 本身就會處理
const { data: room, pending, error } = await useFetch(
  () => `${config.public.apiBase}/hotels/${route.params.id}`
);

// 2. 加入購物車 (訂房) 邏輯
const addToCart = async () => {
    // (A) 檢查是否登入
    if (!authToken.value) {
        Swal.fire({
            icon: 'warning',
            title: '請先登入',
            text: '您需要登入才能預定房間喔！',
            showCancelButton: true,
            confirmButtonText: '前往登入',
            cancelButtonText: '取消'
        }).then((result) => {
            if (result.isConfirmed) {
                router.push('/login'); // 導向登入頁
            }
        });
        return;
    }

    // (B) 跳出 SweetAlert 確認視窗
    const confirmResult = await Swal.fire({
        title: '確定要預定嗎？',
        html: `您即將預定 <b>${room.value.hotel_name}</b><br>價格：$${room.value.price}`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#ffc107', // warning color
        cancelButtonColor: '#6c757d',
        confirmButtonText: '是的，加入購物車！',
        cancelButtonText: '再考慮一下'
    });

    // 如果使用者按取消，就結束
    if (!confirmResult.isConfirmed) return;

    // (C) 發送 API 請求
    isBooking.value = true;

    try {
        // 這裡對應您的 curl 指令
        // POST http://localhost:8000/carts/add/{id}
        await $fetch(`${config.public.apiBase}/carts/add/${route.params.id}`, {
            method: 'POST',
            headers: {
                // 🚨 關鍵：一定要帶 Token 才能通過後端驗證
                'Authorization': `Bearer ${authToken.value}`
            }
        });

        // (D) 成功提示
        Swal.fire({
            icon: 'success',
            title: '加入成功！',
            text: '該房間已加入您的購物車。',
            confirmButtonText: '前往結帳',
            showCancelButton: true,
            cancelButtonText: '繼續逛逛'
        }).then((result) => {
            if (result.isConfirmed) {
                // 假設您的購物車頁面路徑是 /cart 或 /profile
                // 根據您之前的程式碼，應該是導向個人頁面的購物車 tab
                router.push('/about'); 
            }
        });

    } catch (err) {
        console.error('訂房失敗', err);
        
        // 處理錯誤訊息
        let errorMsg = '無法加入購物車，請稍後再試。';
        if (err.response && err.response.status === 401) {
            errorMsg = '登入已過期，請重新登入。';
        } else if (err.data && err.data.detail) {
            errorMsg = err.data.detail; // 顯示後端回傳的具體錯誤
        }

        Swal.fire({
            icon: 'error',
            title: '預定失敗',
            text: errorMsg
        });

    } finally {
        isBooking.value = false;
    }
};
</script>

<style scoped>
/* 讓按鈕內的圖示與文字對齊 */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
</style>