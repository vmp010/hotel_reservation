<template>
    <div class="page-wrapper">
        
        <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
          <div class="container">
            <NuxtLink class="navbar-brand fw-bold" to="/settingHotel" v-if="userState?.role === 'owner'" >旅遊訂房平台</NuxtLink>
            <NuxtLink class="navbar-brand fw-bold" to="/" v-if="userState?.role === 'user'" >旅遊訂房平台</NuxtLink>
            <NuxtLink class="navbar-brand fw-bold" to="/" v-if="!userState">旅遊訂房平台</NuxtLink>

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
                  <NuxtLink class="nav-link" to="/about">個人資料</NuxtLink>
                </li>
                <li class="nav-item" v-if="loggedIn">
                  <button class="nav-link" @click="handleLogout">登出</button> 
                </li>
              </ul>
            </div>
          </div>
        </nav>
        
        <main class="flex-grow-1">
            <slot/>
        </main>

        <footer class="bg-dark text-white py-3 text-center">
          <p class="mb-0">© 2025 旅遊訂房平台 | All Rights Reserved</p>
          <a href="#" ><i class="bi bi-arrow-up-circle h1 position-absolute end-0 me-3"></i></a>
        </footer>
    </div>
</template>

<script setup>
import Swal from 'sweetalert2'; 
import { useRouter } from 'vue-router'; 
import { onMounted } from 'vue'; // 引入 onMounted

// ✨ 核心修正：合併所有來自 useAuth 的導入到一行
import { 
    performLogoutCleanup, 
    useLoggedIn, 
    useUser,
    initializeUserSession // 這是您需要的初始化函式
} from '~/composables/useAuth';

// 取得使用者身份
const userState = useUser();

const router = useRouter();
const loggedIn = useLoggedIn(); 
// 🚩 核心：在組件掛載時，檢查並恢復使用者資料
onMounted(() => {
    initializeUserSession();
});


const handleLogout = async () => {
    const result = await Swal.fire({
        title: '確定要登出嗎？',
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#0d6efd', 
        cancelButtonColor: '#6c757d', 
        confirmButtonText: '是的，登出',
        cancelButtonText: '取消',
    });

    if (result.isConfirmed) {
        performLogoutCleanup();
        await router.push('/'); 
        
        Swal.fire(
            '已登出！',
            '您已成功登出系統。',
            'success'
        );
    }
};
</script>

<style scoped>
/* 🚩 核心 CSS：啟用 Sticky Footer 佈局 */

/* 1. 全域設定：確保 HTML 和 Body 佔據整個視窗高度 */
:global(html),
:global(body) {
    height: 100%;
    margin: 0;
    padding: 0;
}

/* 2. Flex 容器設定：讓整個 Wrapper 垂直排列 */
.page-wrapper {
    min-height: 100vh; /* 確保至少有視窗高度 */
    display: flex;
    flex-direction: column;
}

/* 3. 內容成長：讓 <main> 區域佔據所有剩餘空間 */
/* 這是將 footer 推到底部的關鍵 */
main {
    flex-grow: 1;
}

/* 4. 針對頁腳微調：確保箭頭在頁腳內正確定位 */
footer {
    /* 為了讓箭頭的 position-absolute 能夠正確工作 */
    position: relative; 
}
footer i {
    /* 箭頭的樣式，使用 flex 佈局後，relative/absolute 更容易控制 */
    position: absolute; 
    top: 50%;
    transform: translateY(-50%); /* 垂直居中 */
    right: 1rem;
}
</style>