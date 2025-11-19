<template>
  <div class="container py-5">
    
    <!-- 1. 載入中/未登入的 fallback 畫面 (v-else) -->
    <div v-if="!userState" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-3 text-muted">正在載入使用者資料或您尚未登入...</p>
    </div>

    <!-- 2. 主內容：當 userState 存在時才渲染 (v-if) -->
    <div v-else class="row">
      
      <!-- 左側導覽 -->
      <div class="col-md-4 mb-4">
        <div class="card shadow-sm text-center p-4">
          <img
            src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
            class="rounded-circle mx-auto mb-3"
            alt="User Avatar"
            width="120"
          />
          <!-- 顯示動態資料：使用 || '無資料' 作為 fallback -->
          <h4 class="mb-1">{{ userState.username || '無用戶名' }}</h4>
          <p class="text-muted mb-3">{{ userState.email || '無電子郵件' }}</p>

          <hr />

          <!-- 個人資料區 (部分資料仍是寫死的，待 API 補全) -->
          <div class="text-start px-2 mb-3">
            <p class="mb-1"><strong>角色：</strong>{{ userState.role === 'owner' ? '飯店業者' : '一般用戶' }}</p>
            <p class="mb-1"><strong>電話：</strong>{{ userState.phone || '0912-345-678' }}</p>
            <p class="mb-1"><strong>生日：</strong>{{ userState.birthday || '2000/01/01' }}</p>
            <p class="mb-1"><strong>地址：</strong>{{ userState.address || '台北市中正區' }}</p>
          </div>

          <hr />

          <!-- 導覽按鈕 -->
          <div class="d-grid gap-2">
            <button
              class="btn"
              :class="currentTab === 'cart' ? 'btn-primary' : 'btn-outline-primary'"
              @click="currentTab = 'cart'"
            >
              <i class="bi bi-cart-fill me-2"></i> 購物車
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
              <i class="bi bi-cart-fill me-2"></i> 我的購物車 (靜態範例)
            </h4>

            <ul class="list-group">
              <!-- ... 靜態購物車項目 ... -->
              <li class="list-group-item d-flex justify-content-between align-items-center">豪華雙人房<span class="badge bg-primary rounded-pill">$3200</span></li>
              <li class="list-group-item d-flex justify-content-between align-items-center">海景套房<span class="badge bg-primary rounded-pill">$4500</span></li>
              <li class="list-group-item d-flex justify-content-between align-items-center">家庭四人房<span class="badge bg-primary rounded-pill">$5000</span></li>
            </ul>

            <div class="text-end mt-4">
              <button class="btn btn-success">
                <i class="bi bi-credit-card me-2"></i> 前往結帳
              </button>
            </div>
          </div>

          <!-- 編輯個人資料 -->
          <div v-if="currentTab === 'profile'">
            <h4 class="mb-4">
              <i class="bi bi-pencil-square me-2"></i> 編輯個人資料
            </h4>

            <form @submit.prevent="updateProfile">
              <!-- 表單綁定到 profile ref -->
              <div class="mb-3">
                <label class="form-label">姓名</label>
                <input v-model="profile.name" type="text" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label">Email</label>
                <input v-model="profile.email" type="email" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label">電話</label>
                <input v-model="profile.phone" type="text" class="form-control" />
              </div>
              <div class="mb-3">
                <label class="form-label">地址</label>
                <input v-model="profile.address" type="text" class="form-control" />
              </div>
              <div class="text-end">
                <button class="btn btn-primary">
                  <i class="bi bi-save me-2"></i> 儲存變更
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import { useUser } from '~/composables/useAuth'; // 導入全域 user 狀態

// 1. 執行函式並取得全域狀態的 Ref
const userState = useUser(); 

// 2. 頁面切換狀態
const currentTab = ref("cart"); 

// 3. 表單狀態 (Profile Form State)
const profile = ref({
  name: "載入中...",
  email: "載入中...",
  phone: "",
  address: "",
});

// 4. 使用 watch 監聽 userState 的變化，並同步到 profile 表單
// 這樣即使資料是延遲載入的，表單也會自動更新
watch(userState, (newUser) => {
  if (newUser) {
    // 從 userState 複製資料到 profile 表單
    profile.value.name = newUser.username || '無用戶名';
    profile.value.email = newUser.email || '無電子郵件';
    profile.value.phone = newUser.phone || ''; // 從實際 API 欄位獲取
    profile.value.address = newUser.address || ''; // 從實際 API 欄位獲取
  }
}, { immediate: true }); 

// 5. 處理表單提交 (未來會呼叫 API)
function updateProfile() {
  console.log("資料已更新！(需要呼叫 API 儲存)", profile.value);
  // 這裡應呼叫 updateProfileAPI(profile.value)
}
</script>