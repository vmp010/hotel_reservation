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
import { ref } from 'vue'
import { useRouter } from 'vue-router'
// 1. 引入 initializeUserSession (這是關鍵，用來打 /auth/me)
import { useUser, initializeUserSession } from '~/composables/useAuth';

const router = useRouter()
const config = useRuntimeConfig()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const user = useUser();

const handleLogin = async () => {
    error.value = ''
    success.value = ''
    loading.value = true

    const formData = new FormData();
    formData.append('username', email.value);
    formData.append('password', password.value);

    try {
        // 2. 發送登入請求
        // 這裡不需要接回傳值 (Token)，因為後端會自動 Set-Cookie
        // 只要沒有報錯，就代表登入成功了
        await $fetch(`${config.public.apiBase}/auth/token`, {
            method: 'POST',
            body: formData,
            // 🚨 強制攜帶 (雖然登入是寫入，但加上去保險)
            credentials: 'include'
        })
        
        // 3. 登入成功後，立刻呼叫後端查詢使用者資料
        // 這會打 /auth/me 並更新 user.value
        await initializeUserSession();

        // 檢查是否成功取得使用者資料
        if (!user.value) {
            throw new Error('登入成功，但無法獲取使用者資訊');
        }

        success.value = '登入成功！正在跳轉...';
        
        // 4. 根據角色跳轉
        setTimeout(() => {
            if (user.value.role === 'owner') {
                // 如果是業者，跳轉到管理頁面
                // 使用 window.location.href 強制刷新，確保 Cookie 狀態最乾淨
                window.location.href = '/settingHotel'; 
            } else {
                // 如果是一般人，跳回首頁
                window.location.href = '/';
            }
        }, 500)
        
    } catch (e) {
        console.error(e)
        // 錯誤處理
        const message = e?.data?.detail || '帳號或密碼錯誤'
        error.value = Array.isArray(message) ? message.join(', ') : message
        
        // 清空狀態
        user.value = null;
    } finally {
        loading.value = false
    }
}
</script>