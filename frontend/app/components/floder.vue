<template>
    <header class="bg-light text-center py-5" id="page-header">
        <div class="container">
            <h1 class="display-5 fw-bold">歡迎來到旅遊訂房平台</h1>
            <p class="lead text-muted">
                輕鬆搜尋、比價、訂房，開啟你的完美假期 🌴
            </p>

            <NuxtLink class="btn btn-primary btn-lg mt-3 me-3" to="/homeView" v-if="route.path !== '/settingHotel'">開始找房
            </NuxtLink>

            <button @click="$emit('update-tab', 'AddHotelForm')"
                :class="['btn', currentTab === 'AddHotelForm' ? 'btn-danger' : 'btn-outline-danger']"
                class="btn-lg mt-3 me-3" v-if="route.path === '/settingHotel'">
                新增飯店
            </button>

            <NuxtLink  class="btn btn-warning btn-lg mt-3 me-3" to="/homeView" v-if="route.path !== '/'">
                我的飯店
            </NuxtLink>
            

            <button @click="$emit('update-tab', 'BookingList')"
                class="btn-lg mt-3 me-3" v-if="route.path === '/settingHotel'"
                :class="['btn', currentTab === 'BookingList' ? 'btn-primary' : 'btn-outline-primary']">
                查看預訂名單
            </button>

            <!-- <NuxtLink class="btn btn-danger btn-lg mt-3 me-3" to="/settingHotel" v-if="route.path !=='/settingHotel'">新增/刪除飯店</NuxtLink> -->

        </div>
    </header>
</template>
<script setup>
import { useRoute } from 'vue-router'
import { defineProps, defineEmits } from 'vue';

const route = useRoute()

// 💡 接收父組件傳入的 currentTab 狀態
const props = defineProps({
    currentTab: {
        type: String,
        default: ''
    }
})

// 💡 定義發射事件，讓父組件知道 Tab 改變了
const emit = defineEmits(['update-tab'])

</script>