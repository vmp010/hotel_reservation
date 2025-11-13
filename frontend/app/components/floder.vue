<template>
    <header class="bg-light text-center py-5" id="#">
      <div class="container">
        <h1 class="display-5 fw-bold">歡迎來到旅遊訂房平台</h1>
        <p class="lead text-muted">
          輕鬆搜尋、比價、訂房，開啟你的完美假期 🌴
        </p>
        <!-- <a href="#" class="btn btn-primary btn-lg mt-3">開始找房</a> -->
        <NuxtLink class="btn btn-primary btn-lg mt-3 me-3" to="/homeView">開始找房</NuxtLink>
        <NuxtLink class="btn btn-danger btn-lg mt-3 me-3" to="/createHotel">新增飯店</NuxtLink>
      </div>
    </header>
</template>