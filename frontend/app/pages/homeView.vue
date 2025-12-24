<template>
  <div class="container my-5">
    <div class="row">
      <div class="col-md-3">
        
        <div v-if="!isOwner" class="card p-3 shadow-sm mb-4">
          <h5 class="fw-bold mb-3">🔍 搜尋條件</h5> <div class="mb-3">
              <label class="form-label small text-muted">目的地 / 飯店名稱</label>
              <div class="input-group">
                  <span class="input-group-text bg-white"><i class="bi bi-geo-alt"></i></span>
                  <input 
                      type="text" 
                      class="form-control" 
                      v-model="searchLocation" 
                      placeholder="例如：台北、高雄..."
                  >
              </div>
          </div>

          <div class="mb-3">
              <label class="form-label small text-muted">入住日期 (Check-in)</label>
              <input type="date" class="form-control" v-model="filterDate.start" :min="todayStr">
          </div>
          
          <div class="mb-3">
              <label class="form-label small text-muted">退房日期 (Check-out)</label>
              <input type="date" class="form-control" v-model="filterDate.end" :min="filterDate.start || todayStr">
          </div>
          
          <button class="btn btn-primary w-100" @click="applyDateFilter" :disabled="!isDateValid || isSearching">
              <span v-if="isSearching" class="spinner-border spinner-border-sm me-1"></span>
              <i v-else class="bi bi-search"></i> {{ isSearching ? '搜尋中...' : '開始搜尋' }}
          </button>
          
          <div v-if="dateFilterApplied" class="mt-2 text-center">
              <small class="text-success"><i class="bi bi-check-circle"></i> 已顯示搜尋結果</small>
              <button class="btn btn-link btn-sm text-decoration-none p-0 ms-2" @click="clearDateFilter">
                  清除重置
              </button>
          </div>
      </div>
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
        
        <div v-if="pending || isSearching" class="text-center text-muted py-5">
          <div class="spinner-border text-primary mb-2" role="status"></div>
          <p>資料載入中...</p>
        </div>

        <div v-else-if="!user" class="text-center text-muted py-5">
           <div class="spinner-border text-secondary mb-2" role="status"></div>
           <p>驗證身份中...</p>
        </div>

        <div v-else class="row g-4">
          <div class="col-md-4" v-for="room in filteredRooms" :key="room.id">
            
            <NuxtLink 
                :to="{ 
                    path: `/rooms/${room.id}`, 
                    query: { 
                        start: dateFilterApplied ? filterDate.start : undefined, 
                        end: dateFilterApplied ? filterDate.end : undefined 
                    } 
                }"
                class="card h-100 shadow-sm border-0 room-card text-decoration-none text-dark"
            >
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
            <button v-if="dateFilterApplied" class="btn btn-outline-secondary btn-sm mt-2" @click="clearDateFilter">
                清除篩選條件
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import Swal from 'sweetalert2'; // 引入 SweetAlert2 做提示
import { useUser, initializeUserSession } from '~/composables/useAuth';
import { useApiUrl } from '~/composables/useApiUrl';

definePageMeta({ middleware: 'auth' })
const apiBase = useApiUrl();
const user = useUser();

// --- 日期篩選相關狀態 ---
const todayStr = new Date().toISOString().split('T')[0];
const filterDate = ref({ start: '', end: '' });
const dateFilterApplied = ref(false); // 是否已套用篩選
const isSearching = ref(false);       // 搜尋按鈕的 Loading 狀態
// --- 地點變數 ---
const searchLocation = ref(''); // 📍 儲存地點關鍵字

// 初始化
onMounted(() => {
    initializeUserSession();
});

// 1. 預設載入「全部」飯店 (使用 useFetch)
// server: false 確保在客戶端執行，避免 Docker SSR 問題
const { data: rooms, pending, refresh } = await useFetch(`${apiBase}/hotels`, {
    server: false
});

const isOwner = computed(() => user.value?.role === 'owner');
const selectedCategory = ref('全部')

const categories = computed(() => {
  if (!rooms.value) return []
  return [...new Set(rooms.value.map(r => r.room_type))] 
})

const filterByCategory = (category) => {
  selectedCategory.value = category
}

// 檢查日期是否填寫完整且邏輯正確
const isDateValid = computed(() => {
    return filterDate.value.start && filterDate.value.end && filterDate.value.start < filterDate.value.end;
});

// 🚀 核心功能：呼叫後端搜尋 API
const applyDateFilter = async () => {
    if (!isDateValid.value) return;
    
    isSearching.value = true; // 開啟 Loading

    try {
        // 使用 $fetch 發送 GET 請求 (假設後端 API 路徑是 /hotels/search/)
        // 注意：參數名稱 (checkin_date, checkout_date) 要跟後端定義的一模一樣
        const searchResults = await $fetch(`${apiBase}/hotels/search/`, {
            method: 'GET',
            params: {
                checkin_date: filterDate.value.start,
                checkout_date: filterDate.value.end,
                location: searchLocation.value || undefined // 📍 關鍵：如果有填就傳，沒填就傳 undefined (後端會忽略)
            }
        });

        // ✅ 搜尋成功：用搜尋結果覆蓋目前的 rooms 資料
        rooms.value = searchResults;
        dateFilterApplied.value = true;

        if (searchResults.length === 0) {
             Swal.fire('沒有空房', '試試看調整日期或地點關鍵字。', 'info');
        }

    } catch (err) {
        console.error('搜尋失敗', err);
        Swal.fire('搜尋失敗', err.data?.detail || '系統發生錯誤', 'error');
    } finally {
        isSearching.value = false; // 關閉 Loading
    }
};

// 🚀 清除篩選：恢復顯示全部飯店
const clearDateFilter = () => {
    filterDate.value = { start: '', end: '' };
    searchLocation.value = ''; // 📍 清空地點
    dateFilterApplied.value = false;
    
    // 呼叫 useFetch 提供的 refresh()，重新抓一次 /hotels (全部列表)
    refresh(); 
};

// 前端分類過濾邏輯 (日期過濾已經交給後端處理了)
const filteredRooms = computed(() => {
  if (!rooms.value) return []
  
  let result = rooms.value

  // 1. Owner 過濾 (如果是業者，只看自己的)
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