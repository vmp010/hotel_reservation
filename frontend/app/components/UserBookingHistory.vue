<template>
  <div>
    <h4 class="mb-4">
      <i class="bi bi-clock-history me-2"></i> 歷史訂單紀錄
    </h4>

    <div v-if="pending" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-2 text-muted">載入歷史訂單...</p>
    </div>

    <div v-else-if="error" class="alert alert-danger">
        載入失敗：{{ error.message }}
    </div>

    <div v-else-if="history && history.length > 0">
        <div v-for="order in history" :key="order.booking_id" class="card mb-3 shadow-sm border-0">
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h5 class="fw-bold mb-1">{{ order.hotel_name }}</h5>
                        <p class="text-muted mb-2 small">
                            <i class="bi bi-geo-alt-fill text-danger me-1"></i>{{ order.location }}
                        </p>
                        <div class="badge bg-light text-dark border me-2">
                            {{ order.room_type }}
                        </div>
                        <span class="text-muted small">
                             {{ order.check_in }} ~ {{ order.check_out }}
                        </span>
                    </div>
                    
                    <div class="text-end">
                        <h5 class="fw-bold text-primary mb-1">$ {{ (order.total_price || 0).toLocaleString() }}</h5>
                        <span class="badge" 
                            :class="order.is_active ? 'bg-success' : 'bg-secondary'">
                            {{ order.is_active ? '已付款' : '已取消' }}
                        </span>
                    </div>
                </div>

                <hr class="my-3 opacity-25">

                <div class="d-flex justify-content-end">
                     <NuxtLink :to="`/rooms/${order.hotel_id}`" class="btn btn-sm btn-outline-primary">
                        <i class="bi bi-chat-text me-1"></i> 前往評論
                    </NuxtLink>
                </div>
            </div>
        </div>
    </div>

    <div v-else class="text-center py-5 bg-light rounded">
        <i class="bi bi-clipboard-x display-6 mb-3 text-muted opacity-50"></i>
        <p class="text-muted">目前沒有任何歷史訂單。</p>
    </div>
  </div>
</template>

<script setup>
import { useApiUrl } from '~/composables/useApiUrl'; // 確保路徑正確

const apiBase = useApiUrl();

// 呼叫 GET /bookings/UserHistory
const { data: history, pending, error } = await useFetch('/bookings/UserHistory', {
    baseURL: apiBase,
    key: 'user-booking-history', // 避免快取衝突
    credentials: 'include',      // 必加：帶 Cookie
    lazy: true,                  // 不阻塞頁面載入
    default: () => []            // 預設空陣列
});
</script>