<template>
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <NuxtLink class="navbar-brand fw-bold" to="/" >旅遊訂房平台</NuxtLink>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item" v-if="!loggedIn">
              <NuxtLink class="nav-link" to="/login" >登入</NuxtLink>
            </li>
            <li class="nav-item" v-if="!loggedIn">
              <NuxtLink class="nav-link" to="/register">註冊</NuxtLink>
            </li>
            <li class="nav-item" v-if="loggedIn">
              <NuxtLink class="nav-link" to="/about">人物</NuxtLink>
            </li>
            <li class="nav-item" v-if="loggedIn">
              <button class="nav-link" @click="handleLogout">登出</button> 
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <slot/>
    <footer class="bg-dark text-white py-3 mt-5 position-relative text-center">
      <p class="mb-0">© 2025 旅遊訂房平台 | All Rights Reserved</p>
      <a href="#" ><i class="bi bi-arrow-up-circle h1 position-absolute end-0 me-3 top-50 translate-middle-y"></i></a>
    </footer>
</template>

<script setup>
import Swal from 'sweetalert2'; // ✨ 引入 SweetAlert2
import { useRouter } from 'vue-router'; // 引入 router 進行導航

// ✨ 從 composables/useAuth.js 引入我們需要的東西
import { performLogoutCleanup, useLoggedIn } from '~/composables/useAuth'; 

const router = useRouter();

// 1. 取得全域登入狀態，供模板 v-if 使用 (自動導入)
const loggedIn = useLoggedIn(); 

// 2. 處理帶有 SweetAlert 確認的登出流程
const handleLogout = async () => {
    // 彈出 SweetAlert 確認框
    const result = await Swal.fire({
        title: '確定要登出嗎？',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#0d6efd', // 使用 primary 藍色
        cancelButtonColor: '#6c757d', // 使用 secondary 灰色
        confirmButtonText: '是的，登出',
        cancelButtonText: '取消',
    });

    // 檢查用戶是否點擊「確定」
    if (result.isConfirmed) {
        // 執行登出清理邏輯 (從 Composables 引入)
        performLogoutCleanup();

        // 導航回首頁
        await router.push('/'); 
        
        // 顯示成功訊息 (可選)
        Swal.fire(
            '已登出！',
            '您已成功登出系統。',
            'success'
        );
    }
};
</script>