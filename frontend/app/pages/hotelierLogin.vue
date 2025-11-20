<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4 shadow" style="width: 400px;">
      <h3 class="text-center mb-4 text-success">業者登入</h3>
      <form @submit.prevent="handleLogin">
        <div class="mb-3">
          <label class="form-label">電子郵件</label>
          <!-- 這邊暫時使用 text 等vmp修好api 再改程email -->
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
        <p v-if="success" class="text-success mt-2">{{ success }}</p>
      </form>
      <p class="text-center mt-3">
        還沒有帳號？<NuxtLink to="/registerOwner">註冊</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
// ✨ 從 composables/useAuth.js 引入我們需要的狀態管理
import { useAuthToken, useLoggedIn, useUser } from '~/composables/useAuth';

const router = useRouter()
const config = useRuntimeConfig()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

// 取得 JWT 狀態和 User 狀態
const authToken = useAuthToken();
const loggedIn = useLoggedIn(); // 雖然是 computed，但取得以便查看狀態變化
const user = useUser();


const handleLogin = async () => {
    error.value = ''
    success.value = ''
    
    if (!email.value || !password.value) {
        error.value = '請填寫所有欄位'
        return
    }
    
    loading.value = true
    const formData = new FormData();

    formData.append('username', email.value); // 注意：某些 API 使用 username 欄位來接收 email
    formData.append('password', password.value); // 密碼欄位
    try {
        // 🚩 假設 API /auth/token/ 收到 POST 請求後，返回格式為 { access_token: "..." }
        const res = await $fetch(`${config.public.apiBase}/auth/token`, {
            method: 'POST',
            body: formData,
        })
        
        const token = res.access_token || res.token; 
        if (!token) {
             // 確保 API 真的有回傳 Token
            throw new Error('API 登入成功，但缺少 Token 資訊。');
        }

        // ✨ 核心步驟：儲存 JWT Token 到 Cookie
        authToken.value = token; 
        // 🚨 修正這裡：強制構造完整的 user 物件
        user.value = {
            // 由於 API 沒有直接回傳這些欄位，我們從 Token Payload 和表單輸入推導
            id: res.id || null, 
            username: res.username || email.value.split('@')[0], 
            email: email.value, // 使用表單輸入的 email
            role: res.role || 'owner' // 假設角色為 'owner'
        };
        
        // 舊的 localStorage 邏輯現在由 user 狀態處理，可移除，但為了兼容保留 user 存儲
        if (process.client) {
             localStorage.setItem('user', JSON.stringify(user.value))
        }

        success.value = '登入成功！';
        
        setTimeout(() => {
            router.push('/settingHotel')
        }, 800)
        
    } catch (e) {
        console.error('Login error:', e)
        const message = e?.data?.detail || '登入失敗，請檢查帳號密碼'
        error.value = Array.isArray(message) ? message.join(', ') : message
        
        // 登入失敗時，確保 Cookie 和狀態被清除
        authToken.value = null;
        user.value = null;

    } finally {
        loading.value = false
    }
}
</script>
