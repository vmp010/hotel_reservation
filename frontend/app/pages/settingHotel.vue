<template>
    <Floder
        :current-tab="currentTab" 
        @update-tab="currentTab = $event" 
    />
    
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          
          <AddHotelForm v-if="currentTab === 'AddHotelForm'" /> 
          
          <DelHotelList v-else-if="currentTab === 'DelHotelList'" />

          <div v-else class="text-center text-muted py-5">
            請選擇一個管理選項。
          </div>

        </div>
      </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

// 🚩 3. 關鍵步驟：手動導入您要使用的兩個子組件
// 雖然 Nuxt 默認自動導入，但手動導入可以確保 Vue 能夠明確地找到它們。
import AddHotelForm from '~/components/AddHotelForm.vue';
import DelHotelList from '~/components/DelHotelList.vue';

// 狀態保持不變
const currentTab = ref('AddHotelForm'); 
</script>