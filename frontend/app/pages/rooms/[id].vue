<template>
  <div class="container py-5">
    <NuxtLink to="/homeView" class="btn btn-secondary mt-3">
      <i class="bi bi-arrow-left"></i> 返回列表
    </NuxtLink>

    <div v-if="pending" class="text-center py-5 text-muted">
      <div class="spinner-border text-primary mb-2" role="status"></div>
      <p>資料載入中...</p>
    </div>

    <div v-else-if="room">
      <h1 class="mt-4">{{ room.hotel_name }}</h1>
      
      <div class="row mt-3">
        <div class="col-md-6 mb-4">
            <div class="card shadow-sm p-4 h-100">
                <p class="fs-5">🏠 飯店名稱：<strong>{{ room.hotel_name }}</strong></p>
                <p class="fs-5">📍 地點：{{ room.location }}</p>
                <p class="fs-5">💰 價格：<span class="text-danger fw-bold">${{ room.price }}</span> / 晚</p>
                <p class="fs-5">🛏️ 房型：{{ room.room_type }}</p>
                <hr>
                
                <div v-if="isOwner" class="alert alert-warning">
                    <i class="bi bi-person-workspace me-2"></i> 您是此房型的擁有者
                </div>
                <div v-else class="alert alert-info">
                    <i class="bi bi-info-circle-fill me-2"></i> 請在右側選擇入住與退房日期
                </div>
            </div>
        </div>

        <div class="col-md-6 mb-4">
            
            <div v-if="isOwner" class="card shadow-sm h-100 border-primary">
                <div class="card-header bg-primary text-white fw-bold">
                    <i class="bi bi-gear-fill me-2"></i> 房型管理
                </div>
                <div class="card-body d-flex flex-column justify-content-center align-items-center">
                    
                    <h5 class="text-center text-muted mb-4">您可以對此房型進行以下操作：</h5>

                    <div class="d-grid gap-3 w-100 px-3">
                        <button class="btn btn-outline-primary btn-lg" @click="goToEdit">
                            <i class="bi bi-pencil-square me-2"></i> 編輯房型資訊
                        </button>

                        <button 
                            class="btn btn-outline-danger btn-lg" 
                            @click="deleteThisHotel"
                            :disabled="isDeleting"
                        >
                            <span v-if="isDeleting" class="spinner-border spinner-border-sm me-2"></span>
                            <i v-else class="bi bi-trash3-fill me-2"></i> 
                            {{ isDeleting ? '正在刪除...' : '刪除此房型' }}
                        </button>
                    </div>

                </div>
            </div>

            <div v-else class="card shadow-sm p-4 h-100">
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

// 狀態控制
const isBooking = ref(false);
const isDeleting = ref(false);
const dateRange = ref(null);

// 1. 獲取房間詳細資料
const { data: room, pending } = await useFetch(
  () => `${config.public.apiBase}/hotels/${route.params.id}`
);

const isOwner = computed(() => {
    // 必須符合三個條件：
    // 1. 使用者已登入 (user.value 存在)
    // 2. 房間資料已載入 (room.value 存在)
    // 3. 使用者角色必須是 'owner' (防止 ID 撞號誤判)
    // 4. 使用者 ID 等於 房間的 Owner ID
    if (user.value && room.value) {
        // 🚨 關鍵修正：多加一個 role 的檢查
        const isOwnerRole = user.value.role === 'owner';
        const isIdMatch = user.value.id === room.value.owner_id;
        
        return isOwnerRole && isIdMatch;
    }
    return false;
});

// ==========================================
// Owner 功能區
// ==========================================

// 編輯功能 (暫時用 Alert，您可以改成 router.push('/hotels/edit/' + route.params.id))
const goToEdit = () => {
    // router.push(`/hotels/edit/${route.params.id}`); // 如果您有做編輯頁面的話
    Swal.fire('編輯功能', '這裡未來會跳轉到編輯頁面', 'info');
};

// 刪除此房間
const deleteThisHotel = async () => {
    const result = await Swal.fire({
        title: '確定要刪除嗎？',
        html: `您即將刪除 <b>${room.value.hotel_name}</b><br>此操作無法復原！`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        cancelButtonColor: '#6c757d',
        confirmButtonText: '是的，刪除',
        cancelButtonText: '取消'
    });

    if (!result.isConfirmed) return;

    isDeleting.value = true;
    try {
        await $fetch(`${config.public.apiBase}/hotels/${route.params.id}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });

        Swal.fire('已刪除', '該房型已成功移除。', 'success').then(() => {
            // 刪除後導向回列表或首頁
            router.push('/homeView'); 
        });
    } catch (err) {
        console.error(err);
        Swal.fire('刪除失敗', err.data?.detail || '系統發生錯誤', 'error');
    } finally {
        isDeleting.value = false;
    }
};

// ==========================================
// User 預訂功能區 (保持不變)
// ==========================================

const { data: unavailableData } = await useFetch(
    () => `${config.public.apiBase}/bookings/unavailable_dates/${route.params.id}`,
    { lazy: true, server: false, default: () => [] }
);

const disabledDates = computed(() => {
    if (!unavailableData.value || !Array.isArray(unavailableData.value)) return [];
    return unavailableData.value.map(booking => ({
        start: new Date(booking.checkin_date || booking.check_in), 
        end: new Date(booking.checkout_date || booking.check_out)
    }));
});

const formatDate = (date) => date ? format(new Date(date), 'yyyy-MM-dd') : '';
const calculateNights = computed(() => {
    if (!dateRange.value?.start || !dateRange.value?.end) return 0;
    return differenceInDays(dateRange.value.end, dateRange.value.start);
});

const submitBooking = async () => {
    if (!authToken.value) { /*...*/ return; } // 省略未登入檢查代碼以節省篇幅
    
    // ... 原本的訂房邏輯 ...
    isBooking.value = true;
    try {
        const payload = {
            hotel_id: parseInt(route.params.id),
            checkin_date: formatDate(dateRange.value.start),
            checkout_date: formatDate(dateRange.value.end)
        };

        // 1. 訂房
        await $fetch(`${config.public.apiBase}/bookings/create`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${authToken.value}` },
            body: payload
        });

        // 2. 加入購物車 (失敗不擋流程)
        try {
            await $fetch(`${config.public.apiBase}/carts/add/${route.params.id}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${authToken.value}` }
            });
        } catch (e) {}

        Swal.fire('預訂成功', '我們期待您的光臨！', 'success').then(() => {
            router.push('/about'); 
        });

    } catch (err) {
        console.error(err);
        if (err.response?.status === 400) Swal.fire('慢了一步', '已被預訂', 'error');
        else Swal.fire('失敗', '系統錯誤', 'error');
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