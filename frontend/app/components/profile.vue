<template>
  <div class="container py-5">
    <div class="row">
      <!-- 左側導覽 -->
      <div class="col-md-4 mb-4">
        <div class="card shadow-sm text-center p-4">
          <img
            src="https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
            class="rounded-circle mx-auto mb-3"
            alt="User Avatar"
            width="120"
          />
          <h4 class="mb-1">賴彥光</h4>
          <p class="text-muted mb-3">light@example.com</p>

          <hr />

          <!-- 個人資料區 -->
          <div class="text-start px-2 mb-3">
            <p class="mb-1"><strong>電話：</strong>0912-345-678</p>
            <p class="mb-1"><strong>生日：</strong>2000/01/01</p>
            <p class="mb-1"><strong>地址：</strong>台北市中正區</p>
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
              <i class="bi bi-cart-fill me-2"></i> 我的購物車
            </h4>

            <ul class="list-group">
              <li class="list-group-item d-flex justify-content-between align-items-center">
                豪華雙人房
                <span class="badge bg-primary rounded-pill">$3200</span>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                海景套房
                <span class="badge bg-primary rounded-pill">$4500</span>
              </li>
              <li class="list-group-item d-flex justify-content-between align-items-center">
                家庭四人房
                <span class="badge bg-primary rounded-pill">$5000</span>
              </li>
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
import { ref } from "vue";

const currentTab = ref("cart"); // 預設顯示購物車

const profile = ref({
  name: "賴彥光",
  email: "light@example.com",
  phone: "0912-345-678",
  address: "台北市中正區",
});

function updateProfile() {
  alert("資料已更新！");
}
</script>
