<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4 shadow" style="width: 400px;">
      <h3 class="text-center mb-4">登入帳號</h3>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label class="form-label">電子郵件</label>
          <input v-model="email" type="email" class="form-control" placeholder="輸入 Email" required>
        </div>
        <div class="mb-3">
          <label class="form-label">密碼</label>
          <input v-model="password" type="password" class="form-control" placeholder="輸入密碼" required>
        </div>
        <button type="submit" class="btn btn-primary w-100">登入</button>
      </form>
      <p class="text-center mt-3">
        還沒有帳號？<NuxtLink to="/register">註冊</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')

const handleLogin = () => {
  console.log('登入中...', email.value, password.value)
  // 這裡之後可以呼叫 FastAPI 的 API，例如：
  // await $fetch('/api/login', { method: 'POST', body: { email: email.value, password: password.value } })
}
</script>
