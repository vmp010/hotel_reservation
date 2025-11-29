<template>
    <Floder
        :current-tab="currentTab" 
        @update-tab="currentTab = $event" 
    />
    
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-10"> <AddHotelForm v-if="currentTab === 'AddHotelForm'" /> 
          
          <DelHotelList v-else-if="currentTab === 'DelHotelList'" />

          <OwnerBookingList v-else-if="currentTab === 'BookingList'" />

          <div v-else class="text-center text-muted py-5">
            請選擇一個管理選項。
          </div>

        </div>
      </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

// 手動導入組件
import AddHotelForm from '~/components/AddHotelForm.vue';
import DelHotelList from '~/components/DelHotelList.vue';
// 🚩 導入新做的組件
import OwnerBookingList from '~/components/OwnerBookingList.vue';

// 狀態
const currentTab = ref('AddHotelForm'); 
</script>