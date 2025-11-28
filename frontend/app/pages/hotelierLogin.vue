<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4 shadow" style="width: 400px;">
      <h3 class="text-center mb-4 text-success">業者登入 (重製版)</h3>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label class="form-label">電子郵件</label>
          <input v-model="email" type="email" class="form-control" placeholder="輸入 Email" required>
        </div>
        <div class="mb-3">
          <label class="form-label">密碼</label>
          <input v-model="password" type="password" class="form-control" placeholder="輸入密碼" required>
        </div>
        <button type="submit" class="btn btn-success w-100" :disabled="loading">
          {{ loading ? '登入中...' : '登入' }}
        </button>
        <p v-if="error" class="text-danger mt-2">{{ error }}</p>
      </form>
      <p class="text-center mt-3">
        還沒有帳號？<NuxtLink to="/registerOwner">業主註冊</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthToken, useUser } from '~/composables/useAuth';

const config = useRuntimeConfig()
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

// 引入全域狀態
const authToken = useAuthToken();
const user = useUser();

const handleLogin = async () => {
    error.value = ''
    loading.value = true
    
    const formData = new FormData();
    formData.append('username', email.value);
    formData.append('password', password.value);

    try {
        // 1. 發送請求
        const res = await $fetch(`${config.public.apiBase}/auth/token`, {
            method: 'POST',
            body: formData,
        })
        
        const token = res.access_token;
        if (!token) throw new Error('沒收到 Token');

        // 2. 暴力儲存 Token (同時存 Cookie 和 LocalStorage)
        authToken.value = token;
        if (process.client) {
            localStorage.setItem('manual_token', token); // 備用方案
        }

        // 3. 設定使用者資訊
        user.value = {
            id: res.id,
            username: res.username || email.value,
            role: res.role || 'owner'
        };

        // alert('登入成功！即將跳轉...');
        
        // 4. 最暴力的跳轉方式：直接 reload 整個頁面，強迫 Nuxt 讀取最新 Cookie
        window.location.href = '/settingHotel';

    } catch (e) {
        console.error(e);
        error.value = '登入失敗：' + (e.data?.detail || e.message);
    } finally {
        loading.value = false
    }
}
</script>