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
                    
                    <div v-if="isMyReview(review.user_id)" class="d-flex gap-2">
                        <button 
                            class="btn btn-sm btn-outline-primary border-0"
                            @click="editReview(review)"
                            title="編輯我的評論"
                        >
                            <i class="bi bi-pencil-square"></i>
                        </button>
                        <button 
                            class="btn btn-sm btn-outline-danger border-0"
                            @click="deleteReview(review.id)"
                            title="刪除我的評論"
                        >
                            <i class="bi bi-trash"></i>
                        </button>
                    </div>
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

const props = defineProps({
    hotelId: {
        type: [String, Number],
        required: true
    }
});

// const config = useRuntimeConfig();
const apiBase = useApiUrl();
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

// 編輯評論邏輯 (新增)
const editReview = async (review) => {
    // 1. 彈出編輯視窗 (使用 HTML 自定義表單)
    const { value: formValues } = await Swal.fire({
        title: '編輯評論',
        html: `
            <div class="text-start">
                <div class="mb-3">
                    <label class="form-label fw-bold">評分 (1-5)</label>
                    <select id="swal-edit-rating" class="form-select">
                        <option value="5" ${review.rating === 5 ? 'selected' : ''}>⭐⭐⭐⭐⭐ (5)</option>
                        <option value="4" ${review.rating === 4 ? 'selected' : ''}>⭐⭐⭐⭐ (4)</option>
                        <option value="3" ${review.rating === 3 ? 'selected' : ''}>⭐⭐⭐ (3)</option>
                        <option value="2" ${review.rating === 2 ? 'selected' : ''}>⭐⭐ (2)</option>
                        <option value="1" ${review.rating === 1 ? 'selected' : ''}>⭐ (1)</option>
                    </select>
                </div>
                <div class="mb-3">
                    <label class="form-label fw-bold">評論內容</label>
                    <textarea id="swal-edit-comment" class="form-control" rows="3">${review.comment}</textarea>
                </div>
            </div>
        `,
        focusConfirm: false,
        showCancelButton: true,
        confirmButtonText: '儲存修改',
        cancelButtonText: '取消',
        // 在使用者按下確認時，抓取輸入的值
        preConfirm: () => {
            const ratingStr = document.getElementById('swal-edit-rating').value;
            const comment = document.getElementById('swal-edit-comment').value;

            // 簡單驗證
            if (!comment.trim()) {
                Swal.showValidationMessage('評論內容不能為空');
                return false;
            }

            return {
                rating: parseInt(ratingStr), // API 要求整數
                comment: comment
            };
        }
    });

    // 2. 如果使用者取消，就結束
    if (!formValues) return;

    // 3. 呼叫 API 更新
    try {
        await $fetch(`${apiBase}/reviews/${review.id}`, {
            method: 'PUT',
            body: formValues,
            credentials: 'include' // 確保帶上 Cookie
        });

        Swal.fire('成功', '您的評論已更新', 'success');
        refresh(); // 4. 刷新列表顯示最新內容

    } catch (err) {
        console.error(err);
        Swal.fire('失敗', err.data?.detail || '更新失敗', 'error');
    }
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
        await $fetch(`${apiBase}/reviews/delete/${reviewId}`, {
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