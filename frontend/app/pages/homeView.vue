<template>
  <div class="container my-5">
    <div class="row">
      <div class="col-md-3">
        <div class="card p-3 shadow-sm">
          <h5 class="fw-bold mb-3">房間分類</h5>
          <ul class="list-group list-group-flush">
            <li class="list-group-item" :class="{ active: selectedCategory === '全部' }" @click="filterByCategory('全部')">
              全部房型
            </li>
            <li v-for="category in categories" :key="category" class="list-group-item" :class="{ active: selectedCategory === category }" @click="filterByCategory(category)">
              {{ category }}
            </li>
          </ul>
        </div>
        
        <div v-if="isOwner" class="alert alert-warning mt-3 fade show">
            <small><i class="bi bi-person-badge"></i> 業者模式：僅顯示您的飯店</small>
        </div>
      </div>

      <div class="col-md-9">
        
        <div v-if="pending" class="text-center text-muted py-5">
          <div class="spinner-border text-primary mb-2" role="status"></div>
          <p>資料載入中...</p>
        </div>

        <div v-else-if="!user" class="text-center text-muted py-5">
           <div class="spinner-border text-secondary mb-2" role="status"></div>
           <p>驗證身份中...</p>
        </div>

        <div v-else class="row g-4">
          <div class="col-md-4" v-for="room in filteredRooms" :key="room.id">
            <NuxtLink :to="`/rooms/${room.id}`" class="card h-100 shadow-sm border-0 room-card text-decoration-none text-dark">
              <img src="https://images.unsplash.com/photo-1611892440504-42a792e24d32?q=80&w=600&auto=format&fit=crop" class="card-img-top" alt="Room Image" style="height: 200px; object-fit: cover;">
              <div class="card-body d-flex flex-column"> 
                <h5 class="card-title">{{ room.hotel_name }}</h5>
                <p class="text-muted mb-1">{{ room.location }}</p>
                <p class="fw-bold text-primary mb-3 mt-auto">$ {{ room.price }} / 晚</p>
                <span class="btn w-100" :class="isOwner ? 'btn-outline-warning' : 'btn-outline-primary'">
                  {{ isOwner ? '管理房型' : '查看詳情' }}
                </span>
              </div>
            </NuxtLink>
          </div>

          <div v-if="filteredRooms.length === 0" class="text-center py-5 text-muted">
            <i class="bi bi-search h1"></i>
            <p class="mt-3">沒有符合條件的房型</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUser, initializeUserSession } from '~/composables/useAuth';
// ❌ 移除 jwt-decode
// ❌ 移除 useAuthToken

definePageMeta({ middleware: 'auth' })
const apiBase = useApiUrl();
const user = useUser();

// 初始化狀態 (打 API)
onMounted(() => {
    initializeUserSession();
});

// API 資料 (server: false 避開 Docker 問題)
const { data: rooms, pending, error } = await useFetch(`${apiBase}/hotels`, {
    server: false
});

// 判斷是否為 Owner
const isOwner = computed(() => user.value?.role === 'owner');

const selectedCategory = ref('全部')
const selectedTag = ref(null)

const categories = computed(() => {
  if (!rooms.value) return []
  return [...new Set(rooms.value.map(r => r.room_type))] 
})

const filterByCategory = (category) => {
  selectedCategory.value = category
  selectedTag.value = null
}

const filteredRooms = computed(() => {
  if (!rooms.value) return []
  
  let result = rooms.value

  // 1. Owner 過濾邏輯
  // 這裡加上 user.value 防呆，雖然 template 已經擋了一層，但雙重保險更好
  if (isOwner.value && user.value) {
      const userId = String(user.value.id);
      result = result.filter(r => String(r.owner_id) === userId);
  }

  // 2. 分類篩選
  if (selectedCategory.value !== '全部') {
    result = result.filter(r => r.room_type === selectedCategory.value)
  }

  return result
})
</script>

<style scoped>
.room-card { transition: transform 0.2s ease, box-shadow 0.2s ease; overflow: hidden; }
.card { display: flex; flex-direction: column; }
.room-card:hover { transform: translateY(-5px); box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1); }
.list-group-item { cursor: pointer; }
.list-group-item.active { background-color: #0d6efd; color: white; border-color: #0d6efd; }
</style>