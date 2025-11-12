<template>
  <div class="container py-5">
    <NuxtLink to="/homeView" class="btn btn-secondary mt-3">
      <i class="bi bi-arrow-left"></i> 返回
    </NuxtLink>

    <div v-if="pending" class="text-center py-5 text-muted">
      資料載入中...
    </div>

    <div v-else-if="room">
      <h1 class="mt-4">{{ room.hotel_name }}</h1>
      <!-- <img
        :src="room.image || 'https://via.placeholder.com/800x400?text=Room+Image'"
        class="img-fluid rounded mb-3"
        alt="room"
      /> -->
      <p>🏠 飯店名稱：{{ room.hotel_name }}</p>
      <p>📍 地點：{{ room.location }}</p>
      <p>💰 價格：${{ room.price }} / 晚</p>
      <p>🛏️ 房型：{{ room.room_type }}</p>
    </div>
    

    <div v-else class="text-center text-muted py-5">
      查無此房型 😅
    </div>
    <NuxtLink to="/about" class="btn btn-warning mt-3">
      <i class="bi bi-bag-fill"></i> 預定房間
    </NuxtLink>
  </div>
</template>

<script setup>
const route = useRoute()

// 根據網址中的 id 去 FastAPI 抓資料
const { data: room, pending, error } = await useFetch(
  () => `http://localhost:8000/hotels/${route.params.id}`
)
</script>