<template>
  <div class="card shadow-sm">
    <div class="card-header bg-white py-3 d-flex justify-content-between align-items-center">
      <h5 class="mb-0 fw-bold text-primary">
        <i class="bi bi-calendar-check me-2"></i>房客預訂清單
      </h5>
      <button class="btn btn-sm btn-outline-secondary" @click="refresh">
        <i class="bi bi-arrow-clockwise"></i> 刷新
      </button>
    </div>

    <div class="card-body p-0">
      <div v-if="pending" class="text-center py-5">
        <div class="spinner-border text-primary" role="status"></div>
        <p class="mt-2 text-muted">正在載入訂單資料...</p>
      </div>

      <div v-else-if="error" class="alert alert-danger m-3">
        載入失敗：{{ error.message }}
      </div>

      <div v-else-if="bookings && bookings.length > 0" class="table-responsive">
        <table class="table table-hover align-middle mb-0">
          <thead class="table-light">
            <tr>
              <th scope="col" class="ps-4">#編號</th>
              <th scope="col">預訂飯店 / 房型</th>
              <th scope="col">房客資訊</th>
              <th scope="col">入住 / 退房日期</th>
              <th scope="col">狀態</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in bookings" :key="item.booking_id">
              <td class="ps-4 fw-bold text-secondary">#{{ item.booking_id }}</td>
              
              <td>
                <div class="fw-bold">{{ item.hotel_name }}</div>
                <small class="text-muted">{{ item.room_type }}</small>
              </td>

              <td>
                <div><i class="bi bi-person-fill me-1"></i>{{ item.guest_name }}</div>
                <small class="text-muted text-break">{{ item.guest_email }}</small>
              </td>

              <td>
                <div class="text-success"><i class="bi bi-box-arrow-in-right me-1"></i>{{ item.check_in }}</div>
                <div class="text-danger"><i class="bi bi-box-arrow-right me-1"></i>{{ item.check_out }}</div>
              </td>

              <td>
                <span v-if="item.is_active" class="badge bg-success rounded-pill">已預訂</span>
                <span v-else class="badge bg-secondary rounded-pill">已取消</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="text-center py-5 text-muted">
        <i class="bi bi-inbox display-4"></i>
        <p class="mt-3">目前沒有任何預訂資料</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthToken } from '~/composables/useAuth';

const config = useRuntimeConfig();
const authToken = useAuthToken();

// 呼叫 API: GET /bookings/owner/all
const { data: bookings, pending, error, refresh } = await useFetch(
  `${config.public.apiBase}/bookings/owner/all`,
  {
    headers: {
      'Authorization': `Bearer ${authToken.value}`
    },
    // 如果 Token 沒抓到就不發送請求 (防呆)
    immediate: !!authToken.value
  }
);
</script>