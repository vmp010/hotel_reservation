<template>
  <div class="row mt-3">
    <div class="col-md-6 mb-4">
      <div class="card shadow-sm p-4 h-100">
        <p class="fs-5">🏠 飯店名稱：<strong>{{ room.hotel_name }}</strong></p>
        <p class="fs-5">📍 地點：{{ room.location }}</p>
        <p class="fs-5">💰 價格：<span class="text-danger fw-bold">${{ room.price }}</span> / 晚</p>
        <p class="fs-5">🛏️ 房型：{{ room.room_type }}</p>
        <hr>
        <div v-if="isOwner" class="alert alert-warning">
          <i class="bi bi-person-workspace me-2"></i> 您是此房型的擁有者
        </div>
        <div v-else class="alert alert-info">
          <i class="bi bi-info-circle-fill me-2"></i> 請在右側選擇入住與退房日期
        </div>
      </div>
    </div>

    <div class="col-md-6 mb-4">
      
      <div v-if="isOwner" class="card shadow-sm h-100 border-primary">
        <div class="card-header bg-primary text-white fw-bold">
          <i class="bi bi-gear-fill me-2"></i> 房型管理
        </div>
        <div class="card-body d-flex flex-column justify-content-center align-items-center">
          <h5 class="text-center text-muted mb-4">您可以對此房型進行以下操作：</h5>
          <div class="d-grid gap-3 w-100 px-3">
            <button class="btn btn-outline-primary btn-lg" @click="$emit('edit')">
              <i class="bi bi-pencil-square me-2"></i> 編輯房型資訊
            </button>
            <button class="btn btn-outline-danger btn-lg" @click="$emit('delete')" :disabled="isDeleting">
              <span v-if="isDeleting" class="spinner-border spinner-border-sm me-2"></span>
              <i v-else class="bi bi-trash3-fill me-2"></i> {{ isDeleting ? '刪除中...' : '刪除此房型' }}
            </button>
          </div>
        </div>
      </div>

      <div v-else class="card shadow-sm p-4 h-100">
        <h5 class="mb-3 fw-bold">📅 選擇入住日期</h5>
        <ClientOnly>
          <div class="d-flex justify-content-center">
            <VDatePicker 
                v-model.range="dateRange" 
                mode="date" 
                :disabled-dates="disabledDates" 
                :min-date="new Date()" 
            />
          </div>
        </ClientOnly>
        <div class="mt-4">
          <div v-if="dateRange" class="mb-3 text-center fw-bold text-success">
            已選擇：{{ formatDate(dateRange.start) }} ~ {{ formatDate(dateRange.end) }} <br>
            <small class="text-muted">共 {{ calculateNights }} 晚</small>
          </div>
          <button class="btn btn-warning btn-lg w-100 fw-bold text-dark" @click="handleBooking" :disabled="isBooking || !dateRange">
            <span v-if="isBooking" class="spinner-border spinner-border-sm me-2"></span>
            <i v-else class="bi bi-calendar-check me-2"></i> {{ isBooking ? '預訂處理中...' : '立即預訂' }}
          </button>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'; // ✅ 1. 補上 watch
import { format, differenceInDays } from 'date-fns';

const props = defineProps({
  room: Object,
  isOwner: Boolean,
  disabledDates: Array,
  isDeleting: Boolean,
  isBooking: Boolean,
  initialDates: {
    type: Object,
    default: null
  }
});

const emit = defineEmits(['edit', 'delete', 'book']);

const dateRange = ref({ start: new Date(), end: new Date() });

// ✅ 2. 修改 watch 邏輯加入偵錯
watch(() => props.initialDates, (newDates) => {
  // 🖨️ 印出 Log 確認子元件是否收到
  // console.log('👉 子元件 HotelInfoCard 收到 initialDates 變更:', newDates);

  if (newDates && newDates.start && newDates.end) {
    // console.log('✅ 子元件正在更新 dateRange...');
    
    // 確保轉為 Date 物件 (雖然父元件傳過來應該已經是 Date，但再轉一次保險)
    dateRange.value = {
      start: new Date(newDates.start),
      end: new Date(newDates.end)
    };
  } else {
    // console.log('⚠️ 收到空值或格式不完整的日期');
  }
}, { immediate: true });

const formatDate = (date) => date ? format(new Date(date), 'yyyy-MM-dd') : '';
const calculateNights = computed(() => {
  if (!dateRange.value?.start || !dateRange.value?.end) return 0;
  return differenceInDays(dateRange.value.end, dateRange.value.start);
});

const handleBooking = () => {
    if (dateRange.value) {
        emit('book', {
            start: formatDate(dateRange.value.start),
            end: formatDate(dateRange.value.end)
        });
    }
};
</script>

<style scoped>
.btn { display: inline-flex; align-items: center; justify-content: center; }
</style>