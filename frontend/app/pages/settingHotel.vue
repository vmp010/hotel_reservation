<template>
    <floder
        :current-tab="currentTab" 
        @update-tab="currentTab = $event" 
    />
    
    <div class="container py-5">
      <div class="row justify-content-center">
        <div class="col-lg-8">
          <Transition name="fade" mode="out-in">
             <component :is="currentTab" :key="currentTab" /> 
          </Transition>
        </div>
      </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
// Nuxt 3 會自動導入 PageHeader, AddHotelForm, DelHotelList

const currentTab = ref('AddHotelForm'); 
</script>