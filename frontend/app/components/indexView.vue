<template>
  <section class="py-5">
    <div class="container">
      <h2 class="mb-4 fw-bold">為您推薦</h2>

      <div v-if="pending" class="text-center py-5">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2 text-primary">資料載入中，請稍候...</p>
      </div>

      <div v-else-if="error" class="text-center py-5">
        <p class="text-danger fw-bold">⚠️ 載入資料失敗！</p>
        <p class="text-muted">請檢查您的後端 API (http://localhost:8000) 是否正在運行。</p>
        </div>

      <div v-else-if="rooms && Array.isArray(rooms) && rooms.length > 0" class="row g-4">
        <div class="col-md-4" v-for="room in rooms" :key="room.id">
          <div class="card shadow-sm h-100">
            <img 
              :src="room.image || 'https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=800&q=80'" 
              class="card-img-top room-image" 
              :alt="room.hotel_name" 
            />
            <div class="card-body d-flex flex-column">
              <h5 class="card-title">{{ room.hotel_name }} ({{ room.room_type }})</h5>
              <p class="card-text text-muted">{{ room.location }}</p>
              
              <p class="fw-bold text-primary mt-auto">$ {{ room.price }} / 晚</p>
              <NuxtLink :to="`/rooms/${room.id}`" class="btn btn-outline-primary">
                查看詳情
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
      
      <div v-else class="text-center py-5">
        <p class="text-muted">目前沒有推薦房源。</p>
      </div>
    </div>
  </section>
</template>

<script setup>
import { watch } from 'vue';
const apiBase = useApiUrl()
// 🚀 核心修正：直接將 useFetch 的 data 解構賦值給 rooms
// 因為您的 API 返回的是頂層陣列，而不是 { data: [...] }
const { data: rooms, pending, error } = await useFetch(`${apiBase}/index/`, {
    server: false // <-- 禁用 SSR 階段的資料請求
});
// 💡 監聽 rooms 變量，確保只在數據取得時打印，用於除錯
watch(rooms, (newValue) => {
  if (newValue && Array.isArray(newValue)) {
    // console.log('✅ API 數據已成功取得，項目數:', newValue.length);
  }
}, { immediate: true });
</script>

<style scoped>
/* 確保圖片在卡片內有良好的顯示效果 */
.room-image {
  height: 200px; /* 設定一個固定高度 */
  object-fit: cover; /* 確保圖片覆蓋整個區域並保持比例 */
}

/* 確保卡片在內容多寡不同時保持高度一致 */
.card {
    height: 100%;
}
</style>