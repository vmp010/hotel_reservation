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
                                <button class="btn btn-outline-danger btn-lg" @click="deleteThisHotel"
                                    :disabled="isDeleting">
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
                                <VDatePicker v-model.range="dateRange" mode="date" :disabled-dates="disabledDates"
                                    :min-date="new Date()" />
                            </div>
                        </ClientOnly>
                        <div class="mt-4">
                            <div v-if="dateRange" class="mb-3 text-center fw-bold text-success">
                                已選擇：{{ formatDate(dateRange.start) }} ~ {{ formatDate(dateRange.end) }}
                                <br>
                                <small class="text-muted">共 {{ calculateNights }} 晚</small>
                            </div>
                            <button class="btn btn-warning btn-lg w-100 fw-bold text-dark" @click="submitBooking"
                                :disabled="isBooking || !dateRange">
                                <span v-if="isBooking" class="spinner-border spinner-border-sm me-2"></span>
                                <i v-else class="bi bi-calendar-check me-2"></i>
                                {{ isBooking ? '預訂處理中...' : '立即預訂' }}
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="row mt-4">
                <div class="col-12">
                    <div class="card shadow-sm p-4">
                        <h4 class="fw-bold mb-4">
                            <i class="bi bi-chat-quote-fill me-2 text-primary"></i>住客評論
                        </h4>

                        <div v-if="canReview && !hasReviewed" class="mb-5 p-4 bg-light rounded border">
                            <h6 class="fw-bold mb-3">分享您的住宿體驗</h6>
                            <form @submit.prevent="submitReview">
                                <div class="mb-3">
                                    <label class="form-label d-block">評分</label>
                                    <div class="fs-4 text-warning cursor-pointer">
                                        <i v-for="n in 5" :key="n"
                                            :class="reviewData.rating >= n ? 'bi-star-fill' : 'bi-star'"
                                            @click="reviewData.rating = n" class="me-1" style="cursor: pointer;"></i>
                                    </div>
                                </div>
                                <div class="mb-3">
                                    <label class="form-label">留言內容</label>
                                    <textarea v-model="reviewData.comment" class="form-control" rows="3"
                                        placeholder="房間乾淨嗎？服務如何？" required></textarea>
                                </div>
                                <button type="submit" class="btn btn-primary" :disabled="isSubmittingReview">
                                    {{ isSubmittingReview ? '送出中...' : '送出評論' }}
                                </button>
                            </form>
                        </div>

                        

                        <div v-else-if="hasReviewed" class="alert alert-success text-center">
                            <i class="bi bi-check-circle-fill me-2"></i> 您已評論過此飯店，感謝您的回饋！
                        </div>

                        <div v-else-if="!isOwner" class="alert alert-secondary text-center">
                            <i class="bi bi-lock-fill me-2"></i> 只有實際入住過 (且已退房) 的旅客才能撰寫評論。
                        </div>
                        <hr class="my-5">
                        <ReviewList 
                            :hotel-id="route.params.id" 
                            ref="reviewListRef" 
                            @review-deleted="hasReviewed = false" 
                        />
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
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Swal from 'sweetalert2';
import { useAuthToken, useUser } from '~/composables/useAuth';
import { format, differenceInDays } from 'date-fns';

const route = useRoute();
const router = useRouter();
const config = useRuntimeConfig();
// 定義一個動態的 Base URL
// 如果是在伺服器端 (Docker 內)，就用 host.docker.internal
// 如果是在客戶端 (瀏覽器)，就用 localhost
const apiBase = process.server ? 'http://host.docker.internal:8000' : 'http://localhost:8000';

const authToken = useAuthToken();
const user = useUser();

// 狀態控制
const isBooking = ref(false);
const isDeleting = ref(false);
const dateRange = ref(null);

// 評論相關狀態
const canReview = ref(false);
const hasReviewed = ref(false); // 前端暫存，若送出成功設為 true
const isSubmittingReview = ref(false);
const reviewData = ref({
    rating: 5,
    comment: '',
    booking_id: null // 這是關鍵，必須要有 booking_id 才能送出
});

// 取得ReviewList元件的參照
const reviewListRef = ref(null);

// 1. 獲取房間詳細資料 (開啟 SSR，不加 server: false)
const { data: room, pending } = await useFetch(
  `/hotels/${route.params.id}`, // 這裡只寫路徑
  {
    baseURL: apiBase, // 這裡帶入動態網址
    key: `room-${route.params.id}` // 🚨 關鍵：必須設定 key，不然 Nuxt 會以為前後端資料不一致
  }
);

// 判斷是否為 Owner
const isOwner = computed(() => {
    if (user.value && room.value) {
        return user.value.role === 'owner' && user.value.id === room.value.owner_id;
    }
    return false;
});

// ==========================================
// 🔍 核心邏輯：檢查評論資格 (使用 UserHistory API)
// ==========================================
const checkEligibility = async () => {
    // 如果沒登入或是業者，就不用檢查了
    if (!authToken.value || isOwner.value) return;

    try {
        // 呼叫 UserHistory 取得歷史訂單
        const historyList = await $fetch(`${config.public.apiBase}/bookings/UserHistory`, {
            headers: { 'Authorization': `Bearer ${authToken.value}` }
        });

        // 篩選：找出「這間飯店」的訂單
        // 注意：這裡假設 UserHistory 回傳的 hotel_name 是唯一的，或者最好是有 hotel_id
        const matchedBooking = historyList.find(b => b.hotel_name === room.value.hotel_name);

        if (matchedBooking) {
            canReview.value = true;
            // 抓到 booking_id，之後送出評論要用
            reviewData.value.booking_id = matchedBooking.booking_id;
            console.log('✅ 評論資格符合，Booking ID:', matchedBooking.booking_id);
        } else {
            console.log('❌ 查無此飯店的歷史訂單，無法評論');
            canReview.value = false;
        }

    } catch (e) {
        console.error('檢查評論資格失敗', e);
        canReview.value = false;
    }
};

// 在元件掛載後執行檢查
onMounted(() => {
    if (room.value) {
        checkEligibility();
    }
});

// ==========================================
// 送出評論
// ==========================================
const submitReview = async () => {
    if (!reviewData.value.booking_id) {
        Swal.fire('錯誤', '找不到對應的訂單 ID，無法評論', 'error');
        return;
    }

    isSubmittingReview.value = true;
    try {
        const payload = {
            hotel_id: parseInt(route.params.id),
            booking_id: reviewData.value.booking_id,
            rating: reviewData.value.rating,
            comment: reviewData.value.comment
        };

        await $fetch(`${config.public.apiBase}/reviews/create`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${authToken.value}` },
            body: payload
        });

        Swal.fire('評論成功', '感謝您的回饋！', 'success');
        hasReviewed.value = true; // 隱藏表單

        // 🚀 關鍵：叫子元件重新抓資料
        if (reviewListRef.value) {
            reviewListRef.value.refresh();
        }

    } catch (err) {
        console.error(err);
        Swal.fire('送出失敗', err.data?.detail || '系統發生錯誤', 'error');
    } finally {
        isSubmittingReview.value = false;
    }
};

// ==========================================
// Owner 功能區 (編輯/刪除)
// ==========================================
const goToEdit = () => {
    Swal.fire('編輯功能', '這裡未來會跳轉到編輯頁面', 'info');
};

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
            router.push('/homeView');
        });
    } catch (err) {
        Swal.fire('刪除失敗', err.data?.detail || '系統錯誤', 'error');
    } finally {
        isDeleting.value = false;
    }
};

// ==========================================
// User 預訂功能區 (日曆/訂房)
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
    if (!authToken.value) {
        Swal.fire({
            icon: 'warning', title: '請先登入', text: '您需要登入才能預訂！', showCancelButton: true, confirmButtonText: '前往登入'
        }).then((res) => { if (res.isConfirmed) router.push('/login'); });
        return;
    }

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

        // 2. 加入購物車 (忽略錯誤)
        try {
            await $fetch(`${config.public.apiBase}/carts/add/${route.params.id}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${authToken.value}` }
            });
        } catch (e) { }

        Swal.fire('預訂成功', '我們期待您的光臨！', 'success').then(() => {
            router.push('/about');
        });

    } catch (err) {
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

.cursor-pointer {
    cursor: pointer;
}
</style>