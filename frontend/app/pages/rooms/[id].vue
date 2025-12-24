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

        :initial-dates="prefilledDates"
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
import HotelInfoCard from '~/components/HotelInfoCard.vue';
import HotelReviewSection from '~/components/HotelReviewSection.vue';
import { useApiUrl } from '~/composables/useApiUrl';

const route = useRoute();
const router = useRouter();
const user = useUser();
const apiBase = useApiUrl();
// 狀態恢復
// 🚀 修改重點 2：新增變數來存預填日期
const prefilledDates = ref(null);

onMounted(async () => {
    initializeUserSession();
    
    // 🚀 修改重點 3：一進來就檢查網址有沒有 start 和 end
    if (route.query.start && route.query.end) {
        prefilledDates.value = {
            start: new Date(route.query.start),
            end: new Date(route.query.end)
        };
        //  console.log('抓到預填日期:', prefilledDates.value);
    }
});

// API 資料 (動態 URL 支援 Docker)

const { data: room, pending , refresh } = await useFetch(`/hotels/${route.params.id}`, { 
    baseURL: apiBase, 
    key: `room-${route.params.id}` 
});

// 身分判斷
const isOwner = computed(() => user.value && room.value && user.value.role === 'owner' && user.value.id === room.value.owner_id);

// --- 訂房邏輯 ---
const isBooking = ref(false);
const { data: unavailableData } = await useFetch(() => `${apiBase}/bookings/unavailable_dates/${route.params.id}`, { lazy: true, server: false, default: () => [] ,credentials:'include'});

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
        await $fetch(`${apiBase}/bookings/create`, { 
            method: 'POST', 
            body: payload ,
            credentials: 'include' // 試試看加上這行
        });
        
        try {
            // 🚀 修正：移除 headers
            await $fetch(`${apiBase}/carts/add/${route.params.id}`, { 
                method: 'POST' ,
                credentials: 'include' // 試試看加上這行
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
const goToEdit = async () => {
    // 1. 準備預填資料
    // 注意：Swal 的 input 只能有一個，多個欄位要用 html 手刻
    const { value: formValues } = await Swal.fire({
        title: '編輯房型資訊',
        html: `
            <div class="text-start">
                <div class="mb-3">
                    <label class="form-label fw-bold">飯店名稱</label>
                    <input id="swal-input1" class="form-control" value="${room.value.hotel_name}">
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">地點</label>
                    <input id="swal-input2" class="form-control" value="${room.value.location}">
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">房型</label>
                    <select id="swal-input3" class="form-select">
                        <option value="單人房" ${room.value.room_type === '單人房' ? 'selected' : ''}>單人房</option>
                        <option value="雙人房" ${room.value.room_type === '雙人房' ? 'selected' : ''}>雙人房</option>
                        <option value="四人房" ${room.value.room_type === '四人房' ? 'selected' : ''}>四人房</option>
                        <option value="豪華套房" ${room.value.room_type === '豪華套房' ? 'selected' : ''}>豪華套房</option>
                        <option value="家庭房" ${room.value.room_type === '家庭房' ? 'selected' : ''}>家庭房</option>
                        <option value="總統套房" ${room.value.room_type === '總統套房' ? 'selected' : ''}>總統套房</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">價格</label>
                    <input id="swal-input4" type="number" class="form-control" value="${room.value.price}">
                </div>
            </div>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonText: '儲存變更',
        cancelButtonText: '取消',
        preConfirm: () => {
            // 抓取輸入的值
            return {
                hotel_name: document.getElementById('swal-input1').value,
                location: document.getElementById('swal-input2').value,
                room_type: document.getElementById('swal-input3').value,
                price: parseInt(document.getElementById('swal-input4').value)
            }
        }
    });

    // 2. 如果使用者按了取消，就沒事發生
    if (!formValues) return;

    // 3. 呼叫 API 更新
    try {
        // API 路徑: PATCH /hotels/edit/{hotel_id}
        // 不需要手動加 header，瀏覽器會帶 cookie
        await $fetch(`${apiBase}/hotels/edit/${room.value.id}`, {
            method: 'PATCH',
            body: formValues,
            credentials: 'include' // 確保帶上 Cookie
        });

        // 4. 成功提示
        await Swal.fire('成功', '房型資訊已更新', 'success');
        
        // 5. 刷新頁面資料
        refresh(); // 這是 useFetch 回傳的 refresh 函式

    } catch (err) {
        console.error(err);
        Swal.fire('失敗', err.data?.detail || '更新失敗', 'error');
    }
};

const deleteThisHotel = async () => {
    const result = await Swal.fire({ title: '確定刪除？', icon: 'warning', showCancelButton: true, confirmButtonColor: '#dc3545', confirmButtonText: '刪除' });
    if (!result.isConfirmed) return;

    isDeleting.value = true;
    try {
        // 🚀 修正：移除 headers
        await $fetch(`${apiBase}/hotels/delete/${route.params.id}`, { 
            method: 'DELETE' ,
            credentials : 'include'
        });
        Swal.fire('已刪除', '', 'success').then(() => router.push('/homeView'));
    } catch (err) {
        Swal.fire('失敗', err.data?.detail, 'error');
    } finally {
        isDeleting.value = false;
    }
};
</script>