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
      
      <div class="row mt-3">
        <div class="col-md-6">
            <div class="card shadow-sm p-4 h-100">
                <p class="fs-5">🏠 飯店名稱：<strong>{{ room.hotel_name }}</strong></p>
                <p class="fs-5">📍 地點：{{ room.location }}</p>
                <p class="fs-5">💰 價格：<span class="text-danger fw-bold">${{ room.price }}</span> / 晚</p>
                <p class="fs-5">🛏️ 房型：{{ room.room_type }}</p>
                <hr>
                <div class="alert alert-info">
                    <i class="bi bi-info-circle-fill"></i> 請在右側選擇入住與退房日期
                </div>
            </div>
        </div>

        <div class="col-md-6">
            <div class="card shadow-sm p-4 h-100">
                <h5 class="mb-3 fw-bold">📅 選擇入住日期</h5>
                
                <ClientOnly>
                    <div class="d-flex justify-content-center">
                        <VDatePicker 
                            v-model.range="dateRange" 
                            mode="date"
                            :disabled-dates="disabledDates" 
                            :min-date="new Date()"
                        />
                    </div>
                </ClientOnly>

                <div class="mt-4">
                    <div v-if="dateRange" class="mb-3 text-center fw-bold text-success">
                        已選擇：{{ formatDate(dateRange.start) }} ~ {{ formatDate(dateRange.end) }}
                        <br>
                        <small class="text-muted">共 {{ calculateNights }} 晚</small>
                    </div>

                    <button 
                        class="btn btn-warning btn-lg w-100 fw-bold text-dark" 
                        @click="submitBooking"
                        :disabled="isBooking || !dateRange"
                    >
                        <span v-if="isBooking" class="spinner-border spinner-border-sm me-2"></span>
                        <i v-else class="bi bi-calendar-check me-2"></i> 
                        {{ isBooking ? '預訂處理中...' : '立即預訂' }}
                    </button>
                </div>
            </div>
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
import { ref, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Swal from 'sweetalert2';
import { useAuthToken, useUser } from '~/composables/useAuth';
import { format, differenceInDays } from 'date-fns'; 

const route = useRoute();
const router = useRouter();
const config = useRuntimeConfig();

const authToken = useAuthToken();
const user = useUser();
const isBooking = ref(false);
const dateRange = ref(null);

// 1. 獲取房間詳細資料
const { data: room, pending } = await useFetch(
  () => `${config.public.apiBase}/hotels/${route.params.id}`
);

// 2. 獲取「已被預訂」的日期 (使用 lazy 防止 API 不存在時報錯卡住頁面)
const { data: unavailableData } = await useFetch(
    () => `${config.public.apiBase}/bookings/unavailable_dates/${route.params.id}`,
    {
        lazy: true, // 讓頁面先載入，背景再抓日期
        server: false, // 只在客戶端抓取
        default: () => [] // 預設回傳空陣列
    }
);

// 3. 轉換後端資料給 v-calendar
const disabledDates = computed(() => {
    // 如果 API 還沒回傳或回傳格式不對，就回傳空陣列 (不做禁用)
    if (!unavailableData.value || !Array.isArray(unavailableData.value)) return [];
    
    // 🚨 修正：同時相容 check_in 和 checkin_date 兩種寫法，避免欄位對不上
    return unavailableData.value.map(booking => ({
        start: new Date(booking.checkin_date || booking.check_in), 
        end: new Date(booking.checkout_date || booking.check_out)
    }));
});

// 輔助：格式化日期
const formatDate = (date) => date ? format(new Date(date), 'yyyy-MM-dd') : '';

// 輔助：計算晚數
const calculateNights = computed(() => {
    if (!dateRange.value?.start || !dateRange.value?.end) return 0;
    return differenceInDays(dateRange.value.end, dateRange.value.start);
});

// 4. 送出預訂邏輯
const submitBooking = async () => {
    // (A) 檢查登入
    if (!authToken.value) {
        Swal.fire({
            icon: 'warning',
            title: '請先登入',
            text: '您需要登入才能預訂房間喔！',
            showCancelButton: true,
            confirmButtonText: '前往登入'
        }).then((res) => {
            if (res.isConfirmed) router.push('/login');
        });
        return;
    }

    // (B) 再次確認
    const result = await Swal.fire({
        title: '確認預訂資訊',
        html: `
            <div class="text-start">
                <p>飯店：<b>${room.value.hotel_name}</b></p>
                <p>日期：${formatDate(dateRange.value.start)} ~ ${formatDate(dateRange.value.end)}</p>
                <p>總計：<b>${calculateNights.value} 晚</b></p>
                <p>總價：<b class="text-danger">$${(room.value.price * calculateNights.value).toLocaleString()}</b></p>
            </div>
        `,
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: '確認付款/預訂'
    });

    if (!result.isConfirmed) return;

    // (C) 發送 API (並行處理)
    isBooking.value = true;
    try {
        const payload = {
            hotel_id: parseInt(route.params.id),
            checkin_date: formatDate(dateRange.value.start),
            checkout_date: formatDate(dateRange.value.end)
        };

        // 🚀 關鍵修改：準備兩個請求
        
        // 請求 1: 建立預訂紀錄 (日期)
        const bookingRequest = $fetch(`${config.public.apiBase}/bookings/create`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${authToken.value}` },
            body: payload
        });

        // 請求 2: 加入購物車 (將該房間加入購物車)
        const cartRequest = $fetch(`${config.public.apiBase}/carts/add/${route.params.id}`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${authToken.value}` }
            // 根據您之前的 curl，這裡不需要 body，只要網址帶 ID 即可
        });

        // 🔥 使用 Promise.all 同時發送！(兩個都成功才會往下走)
        await Promise.all([bookingRequest, cartRequest]);

        // (D) 成功
        Swal.fire('預訂成功', '已預訂日期並加入購物車！', 'success').then(() => {
            // 轉跳到訂單頁面或付款頁面
            router.push('/about'); 
        });

    } catch (err) {
        console.error(err);
        
        // 錯誤處理 (只要其中一個失敗就會進來這裡)
        if (err.response && err.response.status === 400) {
            Swal.fire({
                icon: 'error',
                title: '哎呀！慢了一步 😱',
                text: '剛剛您選的時段被別人訂走了，請重新選擇日期。',
                confirmButtonText: '重新選擇'
            }).then(() => {
                 // 重新整理不可用日期
                 refreshNuxtData();
            });
        } else if (err.response && err.response.status === 401) {
            Swal.fire('登入過期', '請重新登入', 'error');
        } else if (err.response && err.response.status === 422) {
            Swal.fire('資料格式錯誤', '請檢查日期格式或後端參數', 'error');
        } else {
            Swal.fire('預訂失敗', '系統發生錯誤，請稍後再試', 'error');
        }
    } finally {
        isBooking.value = false;
    }
};
</script>

<style scoped>
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
}
</style>