<template>
  <div class="container py-5">
    
    <!-- 1. 載入中/未登入的 fallback 畫面 (v-else) -->
    <div v-if="!userState" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-3 text-muted">正在載入使用者資料或您尚未登入...</p>
    </div>

    <!-- 2. 主內容：當 userState 存在時才渲染 (v-if) -->
    <div v-else class="row">
      
      <!-- 左側導覽 (保持不變) -->
      <div class="col-md-4 mb-4">
        <div class="card shadow-sm text-center p-4">
          <img
            src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
            class="rounded-circle mx-auto mb-3"
            alt="User Avatar"
            width="120"
          />
          <h4 class="mb-1">{{ userState.username || '無用戶名' }}</h4>
          <p class="text-muted mb-3">{{ userState.email || '無電子郵件' }}</p>
          <hr />
          <div class="text-start px-2 mb-3">
            <p class="mb-1"><strong>角色：</strong>{{ userState.role === 'owner' ? '飯店業者' : '一般用戶' }}</p>
            <p class="mb-1"><strong>電話：</strong>{{ userState.phone || '0912-345-678' }}</p>
            <p class="mb-1"><strong>生日：</strong>{{ userState.birthday || '2000/01/01' }}</p>
            <p class="mb-1"><strong>地址：</strong>{{ userState.address || '台北市中正區' }}</p>
          </div>
          <hr />
          <div class="d-grid gap-2">
            <button
              class="btn"
              :class="currentTab === 'cart' ? 'btn-primary' : 'btn-outline-primary'"
              @click="currentTab = 'cart'"
            >
              <i class="bi bi-cart-fill me-2"></i> 購物車 ({{ cartItems?.length || 0 }})
            </button>
            <button
              class="btn"
              :class="currentTab === 'profile' ? 'btn-primary' : 'btn-outline-primary'"
              @click="currentTab = 'profile'"
            >
              <i class="bi bi-person-lines-fill me-2"></i> 編輯個人資料
            </button>
          </div>
        </div>
      </div>

      <!-- 右側內容 -->
      <div class="col-md-8">
        <div class="card shadow-sm p-4">
          <!-- 購物車 -->
          <div v-if="currentTab === 'cart'">
            <h4 class="mb-4">
              <i class="bi bi-cart-fill me-2"></i> 我的購物車
            </h4>

            <!-- 載入中狀態 -->
            <div v-if="cartPending" class="text-center text-muted">
                <i class="bi bi-arrow-clockwise h4 spin"></i> 載入購物車項目中...
            </div>
            
            <!-- 錯誤狀態 -->
            <div v-else-if="cartError" class="alert alert-danger text-center">
                載入購物車失敗：{{ cartError.message || 'API 錯誤' }}
            </div>
            
            <!-- 購物車內容 -->
            <ul v-else-if="cartItems && cartItems.length > 0" class="list-group">
                <!-- 🚩 這裡使用 cartItems 進行 v-for 渲染 -->
                <li 
                    v-for="item in cartItems" 
                    :key="item.id" 
                    class="list-group-item d-flex justify-content-between align-items-center"
                >
                    {{ item.hotel_name }} ({{ item.room_type }})
                    <span class="badge bg-primary rounded-pill">$ {{ item.price.toLocaleString() }}</span>
                </li>
            </ul>

            <!-- 購物車為空 -->
            <div v-else class="alert alert-info text-center">
                購物車目前沒有任何項目。
            </div>

            <div class="text-end mt-4">
              <button class="btn btn-success">
                <i class="bi bi-credit-card me-2"></i> 前往結帳 (總計：$ {{ totalCartPrice.toLocaleString() }})
              </button>
            </div>
          </div>

          <!-- 編輯個人資料 (保持不變) -->
          <div v-if="currentTab === 'profile'">
            <h4 class="mb-4">
              <i class="bi bi-pencil-square me-2"></i> 編輯個人資料
            </h4>
            <!-- ... (表單內容) ... -->
            <form @submit.prevent="updateProfile">
              <div class="mb-3"><label class="form-label">姓名</label><input v-model="profile.name" type="text" class="form-control" /></div>
              <div class="mb-3"><label class="form-label">Email</label><input v-model="profile.email" type="email" class="form-control" /></div>
              <div class="mb-3"><label class="form-label">電話</label><input v-model="profile.phone" type="text" class="form-control" /></div>
              <div class="mb-3"><label class="form-label">地址</label><input v-model="profile.address" type="text" class="form-control" /></div>
              <div class="text-end">
                <button class="btn btn-primary"><i class="bi bi-save me-2"></i> 儲存變更</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from "vue";
import { useUser, useLoggedIn } from '~/composables/useAuth'; 

const config = useRuntimeConfig();
const userState = useUser(); 
const isLoggedIn = useLoggedIn();

// 2. 頁面切換狀態
const currentTab = ref("cart"); 

// 3. 表單狀態 (Profile Form State - 保持不變)
const profile = ref({ name: "載入中...", email: "載入中...", phone: "", address: "", });

// 4. 購物車資料獲取邏輯
// 🚩 使用 useAsyncData 進行資料獲取，它會自動使用 $fetch 並帶上 Token
const { 
    data: cartItems, 
    pending: cartPending, 
    error: cartError, 
    refresh: refreshCart 
} = await useAsyncData(
    // 唯一的 key (必須是唯一字串)
    'user-cart-items', 
    // 獲取資料的函式
    () => $fetch(`${config.public.apiBase}/carts/`), 
    {
        // 只有在登入狀態為 true 時才執行 fetch
        lazy: true,
        server: false, // 確保只在客戶端運行（因為它依賴登入狀態和 Token）
        
        // 💡 關鍵：監聽登入狀態和 Tab 切換
        // 只有當 isLoggedIn 變成 true (剛登入) 或 currentTab 切換到 'cart' 時才重新獲取
        watch: [isLoggedIn, currentTab], 

        // 如果請求失敗，預設返回空陣列
        default: () => [] 
    }
);

// 計算購物車總價
const totalCartPrice = computed(() => {
    if (!cartItems.value || cartItems.value.length === 0) return 0;
    return cartItems.value.reduce((sum, item) => sum + (item.price || 0), 0);
});


// 5. 使用 watch 監聽 userState 的變化，並同步到 profile 表單 (保持不變)
watch(userState, (newUser) => {
  if (newUser) {
    profile.value.name = newUser.username || '無用戶名';
    profile.value.email = newUser.email || '無電子郵件';
    profile.value.phone = newUser.phone || ''; 
    profile.value.address = newUser.address || ''; 
    // 💡 登入狀態改變時，強制刷新購物車
    refreshCart(); 
  }
}, { immediate: true }); 

// 6. 處理表單提交 (未來會呼叫 API)
function updateProfile() {
  console.log("資料已更新！(需要呼叫 API 儲存)", profile.value);
}
</script>

<style scoped>
/* 簡單的 CSS 讓載入圖標轉動 */
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
.spin {
  animation: spin 1s linear infinite;
}
</style>