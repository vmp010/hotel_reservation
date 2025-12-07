<template>
  <div class="mt-4">
    <h5 class="fw-bold mb-3">
        <i class="bi bi-chat-dots-fill text-primary me-2"></i>旅客評價 ({{ reviews.length }})
    </h5>

    <div v-if="pending" class="text-center py-3 text-muted">
        <div class="spinner-border spinner-border-sm text-secondary" role="status"></div>
        <span class="ms-2">載入評論中...</span>
    </div>

    <div v-else-if="reviews && reviews.length > 0">
        <div v-for="review in reviews" :key="review.id" class="card mb-3 border-0 shadow-sm bg-light">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center mb-2">
                    <div class="fw-bold text-dark">
                        <i class="bi bi-person-circle me-1 text-secondary"></i>
                        {{ review.username || '匿名旅客' }}
                    </div>
                    
                    <button 
                        v-if="isMyReview(review.user_id)" 
                        class="btn btn-sm btn-outline-danger border-0"
                        @click="deleteReview(review.id)"
                        title="刪除我的評論"
                    >
                        <i class="bi bi-trash"></i>
                    </button>
                </div>

                <div class="d-flex justify-content-between align-items-center mb-2">
                    <div class="text-warning">
                        <i v-for="n in 5" :key="n" :class="review.rating >= n ? 'bi-star-fill' : 'bi-star'"></i>
                    </div>
                    <small class="text-muted">{{ formatDate(review.created_at) }}</small>
                </div>

                <p class="card-text text-secondary mb-0">{{ review.comment }}</p>

                <div v-if="review.reply" class="mt-3 p-3 bg-white rounded border-start border-4 border-primary">
                    <small class="fw-bold text-primary mb-1 d-block">飯店回覆：</small>
                    <p class="mb-0 small text-muted">{{ review.reply }}</p>
                </div>
            </div>
        </div>
    </div>

    <div v-else class="text-center py-4 bg-light rounded text-muted">
        <i class="bi bi-chat-square-text display-6 mb-2 d-block"></i>
        目前還沒有評論，快來搶頭香吧！
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineExpose ,defineEmits } from 'vue';
import { format } from 'date-fns'; 
import Swal from 'sweetalert2';
import { useUser } from '~/composables/useAuth'; // 引入 Auth
// 2. 定義可以發送的事件
const emit = defineEmits(['review-deleted']);
// 定義一個動態的 Base URL
// 如果是在伺服器端 (Docker 內)，就用 host.docker.internal
// 如果是在客戶端 (瀏覽器)，就用 localhost
const apiBase = process.server ? 'http://host.docker.internal:8000' : 'http://localhost:8000';

const props = defineProps({
    hotelId: {
        type: [String, Number],
        required: true
    }
});

const config = useRuntimeConfig();
const user = useUser(); // 取得目前登入者

// 呼叫 API: GET /reviews/{hotel_id}
const { data: reviews, pending, refresh } = await useFetch(
    `/reviews/${props.hotelId}`,
    {
        baseURL: apiBase,
        key: `reviews-${props.hotelId}`, // 🚨 記得加 key
        lazy: true, 
        default: () => []
    }
);

// 判斷是否為自己的評論
const isMyReview = (reviewUserId) => {
    if (!user.value) return false;
    // 比對 user.id
    return String(user.value.id) === String(reviewUserId);
};

// 刪除評論邏輯
const deleteReview = async (reviewId) => {
    const result = await Swal.fire({
        title: '確定刪除？',
        text: '刪除後無法復原喔！',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
        confirmButtonText: '是的，刪除',
        cancelButtonText: '取消'
    });

    if (!result.isConfirmed) return;

    try {
        await $fetch(`${config.public.apiBase}/reviews/delete/${reviewId}`, {
            method: 'DELETE',
            credentials: 'include'
        });

        Swal.fire('已刪除', '您的評論已移除', 'success');
        refresh(); // 重新整理列表

        // 🚨 3. 關鍵修改：告訴父元件「評論刪掉了」！
        emit('review-deleted');

    } catch (err) {
        console.error(err);
        Swal.fire('失敗', err.data?.detail || '刪除失敗', 'error');
    }
};

const formatDate = (dateString) => {
    if (!dateString) return '';
    return format(new Date(dateString), 'yyyy/MM/dd HH:mm');
};

defineExpose({ refresh });
</script>