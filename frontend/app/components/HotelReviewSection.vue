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
// 檢查資格 (修正版：使用數量比對法)
const checkEligibility = async () => {
  // 1. 基本檢查
  if (!userState.value || props.isOwner) return;
  
  try {
    const [historyList, reviewsRes] = await Promise.all([
        $fetch(`${apiBase}/bookings/UserHistory`, {
            server: false, credentials: 'include'
        }),
        $fetch(`${apiBase}/reviews/${props.hotelId}`, { 
            server: false , credentials: 'include'
        }) 
    ]);

    // 2. 找出「這間飯店」我住過的所有訂單
    // 注意：這裡建議可以加一個篩選，只算 "已付款" 或 "已完成" 的訂單
    const myStaysAtThisHotel = historyList.filter(b => 
        String(b.hotel_id) === String(props.hotelId)
    );

    // 3. 找出「這間飯店」我寫過的所有評論
    const myReviewsAtThisHotel = reviewsRes.filter(r => 
        String(r.user_id) === String(userState.value.id)
    );

    // console.log(`在此飯店住宿次數: ${myStaysAtThisHotel.length}, 評論次數: ${myReviewsAtThisHotel.length}`);

    // 4. 核心邏輯：數量比對
    // 如果「評論數」少於「住宿數」，代表還有扣打可以評
    if (myReviewsAtThisHotel.length < myStaysAtThisHotel.length) {
        canReview.value = true;
        hasReviewed.value = false;

        // 5. 綁定 Booking ID (這是此方法的唯一小缺點)
        // 因為不知道哪一筆沒評，我們預設綁定「最新的一筆」或「第一筆」住宿
        // 這樣至少送出時會有一個有效的 booking_id
        if (myStaysAtThisHotel.length > 0) {
            // 假設 API 回傳排序是新的在前面，我們就抓第一筆
            // 或是您可以寫邏輯抓 id 最大的
            bookingId.value = myStaysAtThisHotel[0].booking_id;
        }
        
        // console.log('✅ 尚有未評論的住宿，開放評論。綁定 ID:', bookingId.value);

    } else {
        // 評論數 >= 住宿數，代表都評過了
        // console.log('✅ 所有住宿皆已評論');
        canReview.value = false;
        
        // 如果有住過且評過了，顯示「您已評論過」
        if (myStaysAtThisHotel.length > 0) {
            hasReviewed.value = true;
        }
    }

  } catch (e) { 
      console.error('檢查評論資格失敗:', e); 
  }
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