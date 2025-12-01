<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4 shadow" style="width: 400px;">
      <h3 class="text-center mb-4 text-primary">歡迎登入</h3>
      
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label class="form-label">電子郵件 / 帳號</label>
          <input v-model="email" type="text" class="form-control" placeholder="輸入 Email" required>
        </div>
        <div class="mb-3">
          <label class="form-label">密碼</label>
          <input v-model="password" type="password" class="form-control" placeholder="輸入密碼" required>
        </div>
        
        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          <span v-if="loading" class="spinner-border spinner-border-sm me-2"></span>
          {{ loading ? '登入中...' : '登入' }}
        </button>
        
        <p v-if="error" class="text-danger mt-3 text-center">{{ error }}</p>
        <p v-if="success" class="text-success mt-3 text-center">{{ success }}</p>
      </form>
      
      <p class="text-center mt-3">
        還沒有帳號？
        <NuxtLink to="/register">註冊會員</NuxtLink> | 
        <NuxtLink to="/registerOwner">註冊成為業者</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthToken, useUser } from '~/composables/useAuth';

const router = useRouter()
const config = useRuntimeConfig()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const authToken = useAuthToken();
const user = useUser();

const handleLogin = async () => {
    error.value = ''
    success.value = ''
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
        
        const token = res.access_token || res.token; 
        if (!token) throw new Error('登入失敗，未取得 Token');

        // 2. 寫入 Cookie 並等待 Vue 反應
        authToken.value = token; 
        await nextTick(); 

        // 3. 設定使用者狀態 (包含 role)
        // 這裡很重要：res.role 是後端判斷出來的身分
        user.value = {
            id: res.id, 
            username: res.username || email.value.split('@')[0], 
            email: email.value,
            role: res.role // 這是關鍵！可能是 'user' 或 'owner'
        };
        
        if (process.client) {
             localStorage.setItem('user', JSON.stringify(user.value))
        }

        success.value = '登入成功！正在跳轉...';
        
        // 4. 🚀 核心修改：依據身分分流
        setTimeout(() => {
            if (user.value.role === 'owner') {
                // 如果是業者，跳轉到管理頁面
                // 這裡使用 window.location.href 確保狀態最乾淨 (如同我們之前的修復)
                window.location.href = '/settingHotel'; 
            } else {
                // 如果是一般人，跳回首頁
                window.location.href = '/';
            }
        }, 500)
        
    } catch (e) {
        console.error(e)
        const message = e?.data?.detail || '帳號或密碼錯誤'
        error.value = Array.isArray(message) ? message.join(', ') : message
        
        authToken.value = null;
        user.value = null;
    } finally {
        loading.value = false
    }
}
</script>