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
        
        <div v-if="isOwner" class="alert alert-warning mt-3">
            <small><i class="bi bi-person-badge"></i> 業者模式：僅顯示您的飯店</small>
        </div>
      </div>

      <div class="col-md-9">
        
        <div v-if="pending" class="text-center text-muted py-5">
          <div class="spinner-border text-primary mb-2" role="status"></div>
          <p>資料載入中...</p>
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
              <img 
                src="https://images.unsplash.com/photo-1611892440504-42a792e24d32?q=80&w=600&auto=format&fit=crop" 
                class="card-img-top" 
                alt="Room Image"
                style="height: 200px; object-fit: cover;"
              >
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
import { jwtDecode } from 'jwt-decode'; // 1. 確保引入這個

definePageMeta({ middleware: 'auth' })

// ==========================================
// 🚀 關鍵修正：不要等 onMounted，直接在 setup 階段同步恢復
// ==========================================
const user = useUser();

// 如果 user 還是空的，但我們手上有 Token，馬上解碼塞進去！
// 這樣就不用等 initializeUserSession 慢慢跑
if (!user.value && authToken.value) {
    try {
        const decoded = jwtDecode(authToken.value);
        user.value = {
            id: decoded.id || decoded.user_id,
            username: decoded.sub || decoded.username,
            email: decoded.email,
            role: decoded.role
        };
    } catch (e) { console.error(e); }
}

// 雖然上面做了同步恢復，onMounted 還是留著做雙重保險
onMounted(() => {
    initializeUserSession();
});

// ==========================================
// API 資料 (維持 server: false)
// ==========================================
const { data: rooms, pending, error } = await useFetch('http://127.0.0.1:8000/hotels', {
    server: false
});

// ==========================================
// 邏輯判斷 (現在 user.value 一定有值了)
// ==========================================
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
  // 因為我們在上面已經強制恢復了 user，這裡就不會是 null 了
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
.room-card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  overflow: hidden; 
}
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