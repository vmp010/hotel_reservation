<template>
    <!-- 導覽列 -->
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <a class="" href="#"></a>
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
            <!-- <li class="nav-item">
                <NuxtLink class="nav-link" to="/">首頁</NuxtLink>
            </li> -->
            <!-- <li class="nav-item">
              <NuxtLink class="nav-link" to="/homeView">房型瀏覽</NuxtLink>
            </li> -->
            <li class="nav-item">
              <NuxtLink class="nav-link" to="/login">登入</NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink class="nav-link" to="/register">註冊</NuxtLink>
            </li>
            <li class="nav-item">
              <NuxtLink class="nav-link" to="/about">人物</NuxtLink>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <!-- 主要內容區域 -->
    <slot/>
    <footer class="bg-dark text-white py-3 mt-5 position-relative text-center">

      <p class="mb-0">© 2025 旅遊訂房平台 | All Rights Reserved</p>
      <a href="#" ><i class="bi bi-arrow-up-circle h1 position-absolute end-0 me-3 top-50 translate-middle-y"></i></a>
</footer>
</template>