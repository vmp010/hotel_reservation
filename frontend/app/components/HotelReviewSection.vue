<template>
  <div class="row mt-4">
    <div class="col-12">
      <div class="card shadow-sm p-4">
        <h4 class="fw-bold mb-4"><i class="bi bi-chat-quote-fill me-2 text-primary"></i>住客評論</h4>

        <div v-if="canReview && !hasReviewed" class="mb-5 p-4 bg-light rounded border">
          <h6 class="fw-bold mb-3">分享您的住宿體驗</h6>
          <form @submit.prevent="submitReview">
            <div class="mb-3">
              <label class="form-label d-block">評分</label>
              <div class="fs-4 text-warning cursor-pointer">
                <i v-for="n in 5" :key="n" :class="rating >= n ? 'bi-star-fill' : 'bi-star'" @click="rating = n" class="me-1" style="cursor: pointer;"></i>
              </div>
            </div>
            <div class="mb-3">
              <label class="form-label">留言內容</label>
              <textarea v-model="comment" class="form-control" rows="3" placeholder="服務如何？" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
              {{ isSubmitting ? '送出中...' : '送出評論' }}
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
        <ReviewList :hotel-id="hotelId" ref="reviewListRef" @review-deleted="hasReviewed = false" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
// import { useAuthToken } from '~/composables/useAuth';
import Swal from 'sweetalert2';
import ReviewList from '~/components/ReviewList.vue'; // 確保有引入

const props = defineProps({
  hotelId: [Number, String],
  hotelName: String,
  isOwner: Boolean
});

const config = useRuntimeConfig();
// const authToken = useAuthToken();

const canReview = ref(false);
const hasReviewed = ref(false);
const isSubmitting = ref(false);
const rating = ref(5);
const comment = ref('');
const bookingId = ref(null);
const reviewListRef = ref(null);

// 檢查資格
const checkEligibility = async () => {
  if (!userState.value || props.isOwner) return;
  try {
    const historyList = await $fetch(`${config.public.apiBase}/bookings/UserHistory`, {
    });
    // 注意：這裡假設 UserHistory 回傳的資料有 hotel_name
    const matched = historyList.find(b => b.hotel_name === props.hotelName);
    if (matched) {
      canReview.value = true;
      bookingId.value = matched.booking_id;
    }
  } catch (e) { console.error(e); }
};

onMounted(() => checkEligibility());

const submitReview = async () => {
  isSubmitting.value = true;
  try {
    await $fetch(`${config.public.apiBase}/reviews/create`, {
      method: 'POST',
      body: {
        hotel_id: parseInt(props.hotelId),
        booking_id: bookingId.value,
        rating: rating.value,
        comment: comment.value
      }
    });
    Swal.fire('評論成功', '', 'success');
    hasReviewed.value = true;
    if (reviewListRef.value) reviewListRef.value.refresh();
  } catch (err) {
    Swal.fire('失敗', err.data?.detail || '錯誤', 'error');
  } finally {
    isSubmitting.value = false;
  }
};
</script>