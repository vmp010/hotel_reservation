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
        <ReviewList 
          :hotel-id="hotelId" 
          ref="reviewListRef" 
          @review-deleted="handleReviewDeleted" 
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import Swal from 'sweetalert2';
import ReviewList from '~/components/ReviewList.vue'; 
import { useUser } from '~/composables/useAuth'; // 🚨 修正：引入 useUser

const props = defineProps({
  hotelId: [Number, String],
  hotelName: String,
  isOwner: Boolean
});

// const config = useRuntimeConfig();
const apiBase = useApiUrl();
const userState = useUser(); // 🚨 修正：定義 userState 變數

const canReview = ref(false);
const hasReviewed = ref(false);
const isSubmitting = ref(false);
const rating = ref(5);
const comment = ref('');
const bookingId = ref(null);
const reviewListRef = ref(null);

// 檢查資格
const checkEligibility = async () => {
  // 1. 基本檢查
  if (!userState.value || props.isOwner) return;
  
  try {
    // 2. 平行發送請求：抓「歷史訂單」跟「該飯店所有評論」
    const [historyList, reviewsRes] = await Promise.all([
        $fetch(`${apiBase}/bookings/UserHistory`, {
            server: false, credentials: 'include'
        }),
        $fetch(`${apiBase}/reviews/${props.hotelId}`, { // 假設有這支 API 抓飯店評論
            server: false , credentials: 'include'
        }) 
    ]);

    // 3. 找出「我寫過的所有評論」的 booking_id 集合
    // 假設評論資料裡有 user_id 或 booking_id
    const myReviewBookingIds = reviewsRes
        .filter(r => r.user_id === userState.value.id)
        .map(r => r.booking_id);

    // 4. 篩選出：(是這間飯店) AND (已退房) AND (尚未評論過) 的訂單
    // 注意：這裡假設 UserHistory 裡的 check_out 是過去時間
    const validBooking = historyList.find(b => 
        b.hotel_name === props.hotelName && // 是這間飯店
        !myReviewBookingIds.includes(b.booking_id) // 且 這筆訂單還沒被評論過
    );

    if (validBooking) {
      canReview.value = true;
      bookingId.value = validBooking.booking_id; // 綁定這筆還沒評過的訂單
      console.log('✅ 找到可評論的訂單 ID:', bookingId.value);
    } else {
      console.log('❌ 沒有可評論的訂單 (沒住過 或 全部都評過了)');
      canReview.value = false;
      
      // 如果找不到「未評論」的，但有「已評論」的，我們可以顯示 "您已評論過"
      if (myReviewBookingIds.length > 0) {
          hasReviewed.value = true; 
      }
    }

  } catch (e) { console.error(e); }
};
// 當評論被刪除時觸發
const handleReviewDeleted = async () => {
    // 1. 先把狀態重置
    hasReviewed.value = false;
    
    // 2. 重新檢查資格 (這會去後端抓最新的狀態，發現沒有評論了，就會把 canReview 變回 true)
    await checkEligibility();
};
onMounted(() => checkEligibility());

const submitReview = async () => {
  isSubmitting.value = true;
  try {
    await $fetch(`${apiBase}/reviews/create`, {
      method: 'POST',
      body: {
        hotel_id: parseInt(props.hotelId),
        booking_id: bookingId.value,
        rating: rating.value,
        comment: comment.value
      },
      credentials : 'include'
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