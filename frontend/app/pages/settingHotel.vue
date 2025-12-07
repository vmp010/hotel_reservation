<template>
  <div class="bg-light min-vh-100">
    <div class="container py-5">
      
      <div class="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h2 class="fw-bold text-dark mb-1">飯店管理中心</h2>
          <p class="text-muted mb-0">歡迎回來，管理您的房源與訂單</p>
        </div>
      </div>

      <div class="row g-4">
        
        <div class="col-md-3">
          <div class="card shadow-sm border-0 sticky-top" style="top: 20px; z-index: 1;">
            
            <div class="card-body p-0">
              <div class="p-3 pb-2">
                <small class="text-uppercase text-muted fw-bold" style="font-size: 0.75rem; letter-spacing: 1px;">
                  Management Tools
                </small>
              </div>
              
              <div class="list-group list-group-flush">
                <button 
                  class="list-group-item list-group-item-action py-3 border-0 border-start border-4 d-flex align-items-center"
                  :class="currentTab === 'AddHotelForm' ? 'active-tab' : 'text-secondary'"
                  @click="currentTab = 'AddHotelForm'"
                >
                  <i class="bi bi-plus-circle me-3 fs-5"></i>
                  <span class="fw-bold">新增飯店</span>
                </button>

                <button 
                  class="list-group-item list-group-item-action py-3 border-0 border-start border-4 d-flex align-items-center"
                  :class="currentTab === 'DelHotelList' ? 'active-tab' : 'text-secondary'"
                  @click="currentTab = 'DelHotelList'"
                >
                  <i class="bi bi-building-dash me-3 fs-5"></i>
                  <span class="fw-bold">管理/刪除飯店</span>
                </button>

                <button 
                  class="list-group-item list-group-item-action py-3 border-0 border-start border-4 d-flex align-items-center"
                  :class="currentTab === 'BookingList' ? 'active-tab' : 'text-secondary'"
                  @click="currentTab = 'BookingList'"
                >
                  <i class="bi bi-clipboard-data me-3 fs-5"></i>
                  <span class="fw-bold">查看訂單</span>
                </button>
              </div>
            </div>

            <hr class="my-0 opacity-25">

            <div class="card-body p-0">
              <div class="list-group list-group-flush">
                <NuxtLink 
                  to="/homeView" 
                  class="list-group-item list-group-item-action py-3 border-0 text-dark d-flex align-items-center hover-bg-light"
                >
                  <i class="bi bi-house-door me-3 fs-5 text-primary"></i>
                  <span class="fw-bold">返回前台首頁</span>
                  <i class="bi bi-box-arrow-up-right ms-auto text-muted small"></i>
                </NuxtLink>
              </div>
            </div>

          </div>
        </div>

        <div class="col-md-9">
          <Transition name="fade" mode="out-in">
            
            <div :key="currentTab" class="card shadow border-0 h-100">
              <div class="card-body p-4 p-lg-5">
                
                <AddHotelForm v-if="currentTab === 'AddHotelForm'" />
                <DelHotelList v-else-if="currentTab === 'DelHotelList'" />
                <OwnerBookingList v-else-if="currentTab === 'BookingList'" />
                
                <div v-else class="text-center py-5">
                  <img src="https://cdn-icons-png.flaticon.com/512/7486/7486744.png" width="150" class="mb-3 opacity-50">
                  <h5 class="text-muted">請從左側選擇功能</h5>
                </div>

              </div>
            </div>

          </Transition>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
// 導入組件
import AddHotelForm from '~/components/AddHotelForm.vue';
import DelHotelList from '~/components/DelHotelList.vue';
import OwnerBookingList from '~/components/OwnerBookingList.vue';

const currentTab = ref('AddHotelForm');
</script>

<style scoped>
/* 自定義 Active 樣式：左側有藍色線條，背景淡藍 */
.active-tab {
  background-color: #f0f7ff !important; /* 極淡的藍色背景 */
  color: #0d6efd !important;            /* 藍色文字 */
  border-left-color: #0d6efd !important; /* 左側藍色邊框 */
}

/* 非 Active 的項目左側邊框為透明 */
.list-group-item {
  border-left-color: transparent;
  transition: all 0.2s ease;
}

/* 滑鼠移過去的效果 */
.list-group-item:hover:not(.active-tab) {
  background-color: #f8f9fa;
  color: #000 !important;
}

/* 回首頁按鈕的特殊懸停效果 */
.hover-bg-light:hover {
  background-color: #f8f9fa;
  transform: translateX(5px); /* 微微向右移動，增加互動感 */
}

/* 簡單的淡入動畫 (保留您原本的) */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>