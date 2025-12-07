<template>
  <div class="container py-5">

    <div v-if="!userState" class="text-center py-5">
      <div class="spinner-border text-primary" role="status"></div>
      <p class="mt-3 text-muted">正在載入使用者資料...</p>
    </div>

    <div v-else class="row">

      <div class="col-md-4 mb-4">
        <div class="card shadow-sm text-center p-4">
          <img src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" class="rounded-circle mx-auto mb-3"
            alt="User Avatar" width="120" />
          <h4 class="mb-1">{{ userState.username || '無用戶名' }}</h4>
          <p class="text-muted mb-3">{{ userState.email || '無電子郵件' }}</p>
          <hr />
          <div class="text-start px-2 mb-3">
            <p class="mb-1"><strong>角色：</strong>
                <span :class="userState.role === 'owner' ? 'text-primary fw-bold' : ''">
                    {{ userState.role === 'owner' ? '飯店業者' : '一般用戶' }}
                </span>
            </p>
            <p class="mb-1"><strong>電話：</strong>{{ userState.phone || '0912-345-678' }}</p>
            <p class="mb-1"><strong>生日：</strong>{{ userState.birthday || '2000/01/01' }}</p>
            <p class="mb-1"><strong>地址：</strong>{{ userState.address || '台北市中正區' }}</p>
          </div>
          <hr />
          
          <div class="d-grid gap-2">
            <button 
                v-if="userState.role === 'user'" 
                class="btn" 
                :class="currentTab === 'cart' ? 'btn-primary' : 'btn-outline-primary'"
                @click="currentTab = 'cart'"
            >
              <i class="bi bi-cart-fill me-2"></i> 購物車 ({{ cartItems?.length || 0 }})
            </button>
            
            <button 
                v-if="userState.role === 'owner'" 
                class="btn" 
                :class="currentTab === 'dashboard' ? 'btn-primary' : 'btn-outline-primary'"
                @click="currentTab = 'dashboard'"
            >
                <i class="bi bi-speedometer2 me-2"></i> 業績儀表板
            </button>

            <button class="btn" :class="currentTab === 'profile' ? 'btn-primary' : 'btn-outline-primary'"
              @click="currentTab = 'profile'">
              <i class="bi bi-person-lines-fill me-2"></i> 編輯個人資料
            </button>
          </div>
        </div>
      </div>

      <div class="col-md-8">
        <div class="card shadow-sm p-4 h-100">
          
          <div v-if="currentTab === 'dashboard' && userState.role === 'owner'">
            <h4 class="mb-4 fw-bold text-primary">
                <i class="bi bi-graph-up-arrow me-2"></i>營運概況
            </h4>

            <div class="row g-3 mb-4">
                <div class="col-md-6">
                    <div class="card bg-primary text-white h-100 border-0 shadow-sm">
                        <div class="card-body text-center p-4">
                            <i class="bi bi-building display-4 opacity-50"></i>
                            <h2 class="display-5 fw-bold mt-2">{{ myHotels?.length || 0 }}</h2>
                            <p class="card-text text-white-50">擁有飯店數</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                  <div class="card bg-success text-white h-100 border-0 shadow-sm">
                      <div class="card-body text-center p-4">
                          <i class="bi bi-calendar-check display-4 opacity-50"></i>
                          
                          <h2 class="display-5 fw-bold mt-2">{{ paidBookingsCount }}</h2>
                          
                          <p class="card-text text-white-50">有效訂單數 (已付款)</p>
                      </div>
                  </div>
              </div>
            </div>

            <h5 class="mb-3 fw-bold">快速管理</h5>
            <div class="list-group">
                <NuxtLink to="/settingHotel" class="list-group-item list-group-item-action d-flex justify-content-between align-items-center p-3">
                    <div>
                        <i class="bi bi-pencil-square me-2 text-primary"></i> 
                        <strong>管理我的飯店</strong>
                        <div class="small text-muted ms-4">新增、修改或刪除飯店資訊</div>
                    </div>
                    <i class="bi bi-chevron-right text-muted"></i>
                </NuxtLink>
                <button class="list-group-item list-group-item-action d-flex justify-content-between align-items-center p-3" @click="refreshDashboard">
                    <div>
                        <i class="bi bi-arrow-clockwise me-2 text-success"></i> 
                        <strong>重新整理數據</strong>
                    </div>
                </button>
            </div>
          </div>

          <div v-else-if="currentTab === 'cart' && userState.role === 'user'">
            <h4 class="mb-4">
              <i class="bi bi-cart-fill me-2"></i> 我的購物車
            </h4>

            <div v-if="cartPending" class="text-center text-muted py-5">
              <div class="spinner-border text-primary mb-2" role="status"></div>
              <p>載入購物車...</p>
            </div>

            <div v-else-if="cartError" class="alert alert-danger text-center">
              載入失敗：{{ cartError.message || '無法連線' }}
            </div>

            <ul v-else-if="cartItems && cartItems.length > 0" class="list-group">
              <li v-for="item in cartItems" :key="item.booking_id"
                class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <h5 class="mb-1">{{ item.hotel_name }}</h5>
                  <small class="text-muted">
                    {{ item.room_type }} |
                    {{ item.check_in }} ~ {{ item.check_out }} ({{ item.total_days }}晚)
                  </small>
                </div>
                <div class="d-flex align-items-center">
                  <span class="badge bg-primary rounded-pill me-3 fs-6">
                    $ {{ (item.total_price || 0).toLocaleString() }}
                  </span>
                  <button @click="cancelHotel(item.booking_id, item.hotel_name)" class="btn btn-outline-danger btn-sm" :disabled="isDelete">
                    <i class="bi bi-trash"></i>
                  </button>
                </div>
              </li>
            </ul>

            <div v-else class="alert alert-info text-center">
              購物車目前沒有任何項目。
            </div>

            <div class="text-end mt-4" v-if="cartItems?.length > 0">
              <button class="btn btn-success btn-lg" @click="handleCheckout" :disabled="isCheckingOut">
                <span v-if="isCheckingOut" class="spinner-border spinner-border-sm me-2"></span>
                <i v-else class="bi bi-credit-card me-2"></i> 
                {{ isCheckingOut ? '結帳處理中...' : `前往結帳 (總計：$ ${totalCartPrice.toLocaleString()})` }}
              </button>
            </div>
          </div>

          <div v-else-if="currentTab === 'profile'">
            <h4 class="mb-4">
              <i class="bi bi-pencil-square me-2"></i> 編輯個人資料
            </h4>
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
import { ref, watch, computed, onMounted } from "vue";
import { useRouter } from 'vue-router';
// 1. 移除 useAuthToken
import { useUser, useLoggedIn, initializeUserSession } from '~/composables/useAuth';
import Swal from 'sweetalert2';

const config = useRuntimeConfig();
const userState = useUser();
const isLoggedIn = useLoggedIn();
const router = useRouter();

// 預設 Tab 狀態
const currentTab = ref(''); 

// 資料狀態
const profile = ref({ name: "", email: "", phone: "", address: "" });
const isDelete = ref(false);
const isCheckingOut = ref(false);

// Owner 專用資料
const myHotels = ref([]);
const bookings = ref([]);

// 🚀 新增：計算「已付款」的訂單數量
const paidBookingsCount = computed(() => {
    if (!bookings.value || bookings.value.length === 0) return 0;
    
    // 過濾出 status 為 PAID 的訂單
    return bookings.value.filter(item => 
        item.status && item.status.toUpperCase() === 'PAID'
    ).length;
});

// 初始化邏輯
onMounted(async () => {
    // 確保身分恢復
    await initializeUserSession();
    
    // 如果身分恢復成功 (userState 有值)，載入對應 Tab
    if (userState.value) {
        syncProfileData(userState.value);
        if (userState.value.role === 'owner') {
            currentTab.value = 'dashboard';
            refreshDashboard(); 
        } else {
            currentTab.value = 'cart';
            refreshCart(); 
        }
    }
});

// 監聽 userState 變化 (防止 F5 刷新後資料不同步)
watch(userState, (newUser) => {
    if (newUser) {
        syncProfileData(newUser);
        if (!currentTab.value) {
            currentTab.value = newUser.role === 'owner' ? 'dashboard' : 'cart';
        }
    }
}, { immediate: true });

function syncProfileData(user) {
    profile.value.name = user.username || '無用戶名';
    profile.value.email = user.email || '無電子郵件';
    profile.value.phone = user.phone || '';
    profile.value.address = user.address || '';
}

// ==========================================
// 🟥 Owner 邏輯：儀表板數據
// ==========================================
const refreshDashboard = async () => {
    // 2. 改用 userState 判斷，而不是 authToken
    if (!userState.value) return;
    
    try {
        // 3. 移除 headers，並加上 server: false 確保在瀏覽器端執行
        const [hotelsRes, bookingsRes] = await Promise.all([
            $fetch(`${config.public.apiBase}/hotels/my_hotels`, { server: false ,credentials:'include'}),
            $fetch(`${config.public.apiBase}/bookings/owner/all`, { server: false ,credentials:'include' })
        ]);
        
        myHotels.value = hotelsRes.hotels || [];
        bookings.value = bookingsRes || [];
        
    } catch (e) {
        console.error('儀表板資料載入失敗', e);
    }
};

// ==========================================
// 🟦 User 邏輯：購物車 (使用 useAsyncData)
// ==========================================
const { data: cartItems, pending: cartPending, error: cartError, refresh: refreshCart } = await useAsyncData(
  'user-cart-items',
  async () => {
    // 4. 改用 userState 判斷
    if (!userState.value || userState.value.role !== 'user') return [];
    
    // 5. 移除 headers
    return await $fetch(`${config.public.apiBase}/carts/`, { server: false ,credentials:'include' });
  },
  { lazy: true, server: false, default: () => [] }
);

const totalCartPrice = computed(() => {
  if (!cartItems.value?.length) return 0;
  return cartItems.value.reduce((sum, item) => sum + (item.total_price || 0), 0);
});

// 刪除訂單
const cancelHotel = async (bookingId, hotelName) => {
  const confirmDelete = await Swal.fire({
    title: '確定取消？',
    html: `取消預定 <b>${hotelName}</b>`,
    icon: 'warning',
    showCancelButton: true,
    confirmButtonColor: '#dc3545',
    confirmButtonText: '取消預定'
  });

  if (!confirmDelete.isConfirmed) return;

  isDelete.value = true;
  try {
    // 6. 移除 headers
    await $fetch(`${config.public.apiBase}/carts/delete/${bookingId}`, {
      method: 'DELETE',
      credentials: 'include'
    });
    await refreshCart();
    Swal.fire({ icon: 'success', title: '已取消', timer: 1500, showConfirmButton: false });
  } catch (err) {
    Swal.fire('失敗', err.response?.status === 401 ? '登入過期' : '系統錯誤', 'error');
  } finally {
    isDelete.value = false;
  }
};

// 結帳功能
const handleCheckout = async () => {
    const result = await Swal.fire({
        title: '確定要結帳嗎？',
        html: `總金額：<b class="text-success">$${totalCartPrice.value.toLocaleString()}</b><br>確認後將完成訂單。`,
        icon: 'question',
        showCancelButton: true,
        confirmButtonColor: '#198754', 
        cancelButtonColor: '#6c757d',
        confirmButtonText: '是的，付款',
        cancelButtonText: '再等等'
    });

    if (!result.isConfirmed) return;

    isCheckingOut.value = true;
    try {
        // 7. 移除 headers
        const res = await $fetch(`${config.public.apiBase}/carts/checkout`, {
            method: 'POST',
            credentials: 'include'
        });

        await Swal.fire({
            icon: 'success',
            title: '付款成功！',
            text: res.message || '您的訂單已完成，感謝您的預訂！',
            confirmButtonText: '太棒了'
        });

        refreshCart();

    } catch (err) {
        console.error('結帳失敗', err);
        Swal.fire({
            icon: 'error',
            title: '結帳失敗',
            text: err.data?.detail || '系統發生錯誤，請稍後再試。'
        });
    } finally {
        isCheckingOut.value = false;
    }
};

function updateProfile() {
  console.log("資料已更新！", profile.value);
  Swal.fire('成功', '個人資料已更新 (模擬)', 'success');
}
</script>