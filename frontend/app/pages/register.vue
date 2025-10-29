<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4 shadow" style="width: 400px;">
      <h3 class="text-center mb-4 text-primary">註冊帳號</h3>
      <form @submit.prevent="handleregister">
        <div class="mb-3">
          <label class="form-label">電子郵件</label>
          <input v-model="email" type="email" class="form-control" placeholder="輸入 Email" required>
        </div>
        <div class="mb-3">
          <label class="form-label">使用者名稱</label>
          <input v-model="username" type="text" class="form-control" placeholder="輸入使用者名稱" required>
        </div>
        <div class="mb-3">
          <label class="form-label">密碼</label>
          <input v-model="password" type="password" class="form-control" placeholder="輸入密碼" required>
        </div>
        <div class="mb-3">
          <label class="form-label">確認密碼</label>
          <input v-model="confirm_password" type="password" class="form-control" placeholder="再次輸入密碼" required>
        </div>
        <button type="submit" class="btn btn-primary w-100">註冊</button>
      </form>
      <p class="text-center mt-3">
        已經有帳號了？<NuxtLink to="/login">登入</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const email = ref('')
const password = ref('')
const confirm_password = ref('')

const handleregister = () => {
  console.log('註冊中...', email.value, password.value ,confirm_password.value)
  // 這裡之後可以呼叫 FastAPI 的 API，例如：
  // await $fetch('/api/login', { method: 'POST', body: { email: email.value, password: password.value } })
}
</script>
