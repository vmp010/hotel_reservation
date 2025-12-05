<template>
  <div class="container py-5">
    <NuxtLink to="/homeView" class="btn btn-secondary mt-3">
      <i class="bi bi-arrow-left"></i> 返回列表
    </NuxtLink>

    <div v-if="pending" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="room">
      <h1 class="mt-4">{{ room.hotel_name }}</h1>

      <HotelInfoCard 
        :room="room" 
        :is-owner="isOwner" 
        :disabled-dates="disabledDates"
        :is-booking="isBooking"
        :is-deleting="isDeleting"
        @edit="goToEdit"
        @delete="deleteThisHotel"
        @book="submitBooking"
      />

      <HotelReviewSection 
        :hotel-id="room.id" 
        :hotel-name="room.hotel_name" 
        :is-owner="isOwner" 
      />
    </div>

    <div v-else class="text-center py-5 text-muted">查無此房型 😅</div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import Swal from 'sweetalert2';
import { useUser, initializeUserSession } from '~/composables/useAuth';
// ❌ 移除 useAuthToken 和 jwt-decode

// 引入元件
import HotelInfoCard from '~/components/HotelInfoCard.vue';
import HotelReviewSection from '~/components/HotelReviewSection.vue';

const route = useRoute();
const router = useRouter();
const config = useRuntimeConfig();
const user = useUser();

// 狀態恢復
onMounted(() => initializeUserSession());

// API 資料 (動態 URL 支援 Docker)
const apiBase = process.server ? 'http://host.docker.internal:8000' : 'http://localhost:8000';
const { data: room, pending } = await useFetch(`/hotels/${route.params.id}`, { 
    baseURL: apiBase, 
    key: `room-${route.params.id}` 
});

// 身分判斷
const isOwner = computed(() => user.value && room.value && user.value.role === 'owner' && user.value.id === room.value.owner_id);

// --- 訂房邏輯 ---
const isBooking = ref(false);
const { data: unavailableData } = await useFetch(() => `${config.public.apiBase}/bookings/unavailable_dates/${route.params.id}`, { lazy: true, server: false, default: () => [] });

const disabledDates = computed(() => {
    return (unavailableData.value || []).map(b => ({ 
        start: new Date(b.checkin_date || b.check_in), 
        end: new Date(b.checkout_date || b.check_out) 
    }));
});

const submitBooking = async ({ start, end }) => {
    // 檢查登入 (依靠 user 狀態)
    if (!user.value) {
        Swal.fire({ icon: 'warning', title: '請先登入', showCancelButton: true, confirmButtonText: '登入' })
            .then(res => { if(res.isConfirmed) router.push('/login'); });
        return;
    }

    isBooking.value = true;
    try {
        const payload = { hotel_id: parseInt(route.params.id), checkin_date: start, checkout_date: end };
        
        // 🚀 修正：移除 headers，瀏覽器自動帶 Cookie
        await $fetch(`${config.public.apiBase}/bookings/create`, { 
            method: 'POST', 
            body: payload 
        });
        
        try {
            // 🚀 修正：移除 headers
            await $fetch(`${config.public.apiBase}/carts/add/${route.params.id}`, { 
                method: 'POST' 
            });
        } catch(e) {}

        Swal.fire('成功', '預訂成功！', 'success').then(() => router.push('/about'));
    } catch (err) {
        if (err.response?.status === 400) Swal.fire('慢了一步', '已被預訂', 'error');
        else Swal.fire('錯誤', '系統錯誤', 'error');
    } finally {
        isBooking.value = false;
    }
};

// --- 管理邏輯 ---
const isDeleting = ref(false);
const goToEdit = () => Swal.fire('編輯', '施工中', 'info');

const deleteThisHotel = async () => {
    const result = await Swal.fire({ title: '確定刪除？', icon: 'warning', showCancelButton: true, confirmButtonColor: '#dc3545', confirmButtonText: '刪除' });
    if (!result.isConfirmed) return;

    isDeleting.value = true;
    try {
        // 🚀 修正：移除 headers
        await $fetch(`${config.public.apiBase}/hotels/${route.params.id}`, { 
            method: 'DELETE' 
        });
        Swal.fire('已刪除', '', 'success').then(() => router.push('/homeView'));
    } catch (err) {
        Swal.fire('失敗', err.data?.detail, 'error');
    } finally {
        isDeleting.value = false;
    }
};
</script>