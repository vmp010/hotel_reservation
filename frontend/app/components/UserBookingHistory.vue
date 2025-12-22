<template>
  <div>
    <h4 class="mb-4 fw-bold">
      <i class="bi bi-journal-text me-2"></i> 我的訂單管理
    </h4>

    <ul class="nav nav-tabs mb-4">
      <li class="nav-item">
        <button 
          class="nav-link" 
          :class="{ active: activeSubTab === 'upcoming' }"
          @click="activeSubTab = 'upcoming'"
        >
          <i class="bi bi-calendar-event me-2"></i>即將入住
        </button>
      </li>
      <li class="nav-item">
        <button 
          class="nav-link" 
          :class="{ active: activeSubTab === 'history' }"
          @click="activeSubTab = 'history'"
        >
          <i class="bi bi-clock-history me-2"></i>歷史紀錄
        </button>
      </li>
    </ul>

    <div v-if="pending" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-2 text-muted">正在載入訂單資料...</p>
    </div>

    <div v-else>
        
        <div v-if="activeSubTab === 'upcoming'">
            <div v-if="upcomingList && upcomingList.length > 0">
                <div v-for="order in upcomingList" :key="order.booking_id" class="card mb-3 shadow-sm border-0 border-start border-5 border-success">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <div>
                                <h5 class="fw-bold mb-1 text-success">{{ order.hotel_name }}</h5>
                                <p class="text-muted mb-2 small">
                                    <i class="bi bi-geo-alt-fill text-danger me-1"></i>{{ order.location }}
                                </p>
                                <div class="badge bg-success bg-opacity-10 text-success border border-success me-2">
                                    {{ order.room_type }}
                                </div>
                                <span class="fw-bold text-dark">
                                     {{ order.check_in }} ~ {{ order.check_out }}
                                </span>
                            </div>
                            <div class="text-end">
                                <h4 class="fw-bold text-dark mb-1">$ {{ (order.total_price || 0).toLocaleString() }}</h4>
                                <span class="badge bg-success">已付款 / 等待入住</span>
                            </div>
                        </div>
                        <hr class="my-3 opacity-25">
                        <div class="d-flex justify-content-end gap-2">
                             <NuxtLink :to="`/rooms/${order.hotel_id}`" class="btn btn-sm btn-primary">
                                查看飯店詳情
                             </NuxtLink>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="text-center py-5 bg-light rounded">
                <i class="bi bi-calendar-x display-6 mb-3 text-muted opacity-50"></i>
                <p class="text-muted">目前沒有即將入住的行程。</p>
                <NuxtLink to="/homeView" class="btn btn-outline-primary mt-2">去逛逛飯店</NuxtLink>
            </div>
        </div>

        <div v-if="activeSubTab === 'history'">
            <div v-if="historyList && historyList.length > 0">
                <div v-for="order in historyList" :key="order.booking_id" class="card mb-3 shadow-sm border-0 bg-light">
                    <div class="card-body">
                        <div class="d-flex justify-content-between align-items-start">
                            <div class="opacity-75">
                                <h5 class="fw-bold mb-1">{{ order.hotel_name }}</h5>
                                <span class="text-muted small d-block mb-1">
                                     {{ order.check_in }} ~ {{ order.check_out }}
                                </span>
                                <div class="badge bg-secondary text-white">
                                    {{ order.room_type }}
                                </div>
                            </div>
                            <div class="text-end">
                                <h5 class="fw-bold text-muted mb-1">$ {{ (order.total_price || 0).toLocaleString() }}</h5>
                                <span class="badge bg-secondary">已完成</span>
                            </div>
                        </div>
                        <hr class="my-3 opacity-25">
                        <div class="d-flex justify-content-end">
                            <NuxtLink :to="`/rooms/${order.hotel_id}`" class="btn btn-sm btn-outline-secondary">
                                <i class="bi bi-chat-text me-1"></i> 前往評論
                            </NuxtLink>
                        </div>
                    </div>
                </div>
            </div>
            <div v-else class="text-center py-5 bg-light rounded">
                <i class="bi bi-archive display-6 mb-3 text-muted opacity-50"></i>
                <p class="text-muted">沒有歷史訂單紀錄。</p>
            </div>
        </div>

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useApiUrl } from '~/composables/useApiUrl';

const apiBase = useApiUrl();
const activeSubTab = ref('upcoming'); // 預設顯示即將入住

// 使用 useAsyncData 一次抓取兩支 API
// 1. /bookings/myRes (即將入住)
// 2. /bookings/UserHistory (歷史紀錄)
const { data, pending } = await useAsyncData('user-all-bookings', async () => {
    const [upcoming, history] = await Promise.all([
        $fetch(`${apiBase}/bookings/myRes`, { credentials: 'include' }).catch(() => []),
        $fetch(`${apiBase}/bookings/UserHistory`, { credentials: 'include' }).catch(() => [])
    ]);
    return { upcoming, history };
}, { 
    lazy: true,
    default: () => ({ upcoming: [], history: [] })
});

// 為了方便 template 使用，拆分成兩個變數
const upcomingList = computed(() => data.value?.upcoming || []);
const historyList = computed(() => data.value?.history || []);
</script>

<style scoped>
.nav-tabs .nav-link {
    color: #6c757d;
    cursor: pointer;
}
.nav-tabs .nav-link.active {
    color: #0d6efd;
    font-weight: bold;
    border-bottom: 3px solid #0d6efd; /* 讓選中的 Tab 下面有藍線 */
    background-color: transparent;
    border-top: none;
    border-left: none;
    border-right: none;
}
</style>