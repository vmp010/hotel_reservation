<template>
    <!-- 導覽列 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <a class="navbar-brand fw-bold" href="#">旅遊訂房平台</a>
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
            <li class="nav-item">
                <NuxtLink class="nav-link" to="/">首頁</NuxtLink>
            </li>
            <li class="nav-item"><a class="nav-link" href="#">房型瀏覽</a></li>
            <li class="nav-item">
                <NuxtLink class="nav-link" to="/login">登入</NuxtLink>
            </li>
            <li class="nav-item"><a class="nav-link" href="#">註冊</a></li>
          </ul>
        </div>
      </div>
    </nav>
    <!-- 主要內容區域 -->
    <slot/>
    <footer class="bg-dark text-white text-center py-3 mt-5">
      <p class="mb-0">© 2025 旅遊訂房平台 | All Rights Reserved</p>
    </footer>
</template>