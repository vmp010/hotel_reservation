<template>
  <div class="container my-5">
    <div class="row">
      <!-- 左側分類欄 -->
      <div class="col-md-3">
        <div class="card p-3 shadow-sm">
          <h5 class="fw-bold mb-3">房間分類</h5>
          <ul class="list-group list-group-flush">
            <li
              class="list-group-item"
              :class="{ active: selectedCategory === '全部' }"
              @click="filterByCategory('全部')"
            >
              全部房型
            </li>
            <li
              v-for="category in categories"
              :key="category"
              class="list-group-item"
              :class="{ active: selectedCategory === category }"
              @click="filterByCategory(category)"
            >
              {{ category }}
            </li>
          </ul>

          <!-- <hr class="my-4" /> -->

          <!-- <h5 class="fw-bold mb-3">熱門標籤</h5>
          <div>
            <span
              v-for="tag in tags"
              :key="tag"
              class="badge bg-secondary me-2 mb-2"
              @click="filterByTag(tag)"
              style="cursor: pointer;"
            >
              {{ tag }}
            </span>
          </div> -->
        </div>
      </div>

      <!-- 右側房型卡片 -->
      <div class="col-md-9">
        <div v-if="pending" class="text-center text-muted py-5">
          資料載入中...
        </div>

        <div v-else class="row g-4">
          <div
            class="col-md-4"
            v-for="room in filteredRooms"
            :key="room.id"
          >
            <div class="card h-100 shadow-sm border-0 room-card">
              <!-- 圖片之後記得寫死 -->
              <!-- <img
                :src="room.image || defaultImage"
                class="card-img-top"
                :alt="room.hotel_name"
              /> -->
              <div class="card-body">
                <h5 class="card-title">{{ room.hotel_name }}</h5>
                <p class="text-muted mb-1">{{ room.location }}</p>
                <p class="fw-bold text-primary mb-3">$ {{ room.price }} / 晚</p>
                <NuxtLink
                  :to="`/rooms/${room.id}`"
                  class="btn btn-outline-primary w-100"
                >
                  查看詳情
                </NuxtLink>
              </div>
            </div>
          </div>

          <div v-if="filteredRooms.length === 0" class="text-center py-5 text-muted">
            沒有符合條件的房型 😅
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

// 若要登入後才能瀏覽，可開啟中介軟體
definePageMeta({ middleware: 'auth' })

// 預設圖片
// const defaultImage = 'https://via.placeholder.com/400x300?text=Room'

// 🔹 從 FastAPI 取得房型資料
// 假設 FastAPI 回傳的是像這樣：
// [
//   { id: 2, location: "台北市中正區", price: 3200, room_type: "雙人房", hotel_name: "彥光汽車旅館" }
// ]
const { data: rooms, pending, error } = await useFetch('http://127.0.0.1:8000/hotels')

// 🔹 篩選條件
const selectedCategory = ref('全部')
const selectedTag = ref(null)

// 🔹 先檢查 rooms 是否有值
const categories = computed(() => {
  if (!rooms.value) return []
  return [...new Set(rooms.value.map(r => r.room_type))] // 從 FastAPI 拿 room_type
})

// 🔹 模擬熱門標籤（之後可從後端提供 tags 欄位）
const tags = ref(['海景', '市中心', '平價', '家庭', '高樓層'])

// 🔹 篩選函式
const filterByCategory = (category) => {
  selectedCategory.value = category
  selectedTag.value = null
}
const filterByTag = (tag) => {
  selectedTag.value = tag
  selectedCategory.value = '全部'
}

// 🔹 篩選後房型
const filteredRooms = computed(() => {
  if (!rooms.value) return []
  let result = rooms.value

  if (selectedCategory.value !== '全部') {
    result = result.filter(r => r.room_type === selectedCategory.value)
  }

  return result
})
</script>

<style scoped>
.room-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.room-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
}
.list-group-item {
  cursor: pointer;
}
.list-group-item.active {
  background-color: #0d6efd;
  color: white;
  border-color: #0d6efd;
}
</style>
