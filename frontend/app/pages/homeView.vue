<template>
  <div class="container my-5">
    <div class="row">
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
        </div>
      </div>

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
            <NuxtLink
              :to="`/rooms/${room.id}`"
              class="card h-100 shadow-sm border-0 room-card text-decoration-none text-dark"
            >
              <div class="card-body d-flex flex-column"> 
                <h5 class="card-title">{{ room.hotel_name }}</h5>
                <p class="text-muted mb-1">{{ room.location }}</p>
                <p class="fw-bold text-primary mb-3 mt-auto">$ {{ room.price }} / 晚</p>
                
                <span class="btn btn-outline-primary w-100">
                  查看詳情
                </span>
              </div>
            </NuxtLink>
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
// ... <script setup> 保持不變 ...
import { ref, computed } from 'vue'

definePageMeta({ middleware: 'auth' })

const { data: rooms, pending, error } = await useFetch('http://127.0.0.1:8000/hotels')

const selectedCategory = ref('全部')
const selectedTag = ref(null)

const categories = computed(() => {
  if (!rooms.value) return []
  return [...new Set(rooms.value.map(r => r.room_type))] 
})

const tags = ref(['海景', '市中心', '平價', '家庭', '高樓層'])

const filterByCategory = (category) => {
  selectedCategory.value = category
  selectedTag.value = null
}
const filterByTag = (tag) => {
  selectedTag.value = tag
  selectedCategory.value = '全部'
}

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
/* 讓 NuxtLink 保持區塊行為，確保 h-100 有效 */
.card { 
    display: flex;
    flex-direction: column;
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