<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4 shadow" style="width: 400px;">
      <h3 class="text-center mb-4 text-success">登入帳號</h3>
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
        <p v-if="success" class="text-success mt-2">{{ success }}</p>
      </form>
      <p class="text-center mt-3">
        還沒有帳號？<NuxtLink to="/register">註冊</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const config = useRuntimeConfig()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')
// loggedIn 用來判斷是否登入，才可能進去開始找房
const loggedIn = useState('loggedIn')


const handleLogin = async () => {
    error.value = ''
    success.value = ''
    
    if (!email.value || !password.value) {
        error.value = '請填寫所有欄位'
        return
    }
    
    loading.value = true
    // ⚠️ 移除：loggedIn.value = true 
    
    try {
        const res = await $fetch(`${config.public.apiBase}/login/`, {
            method: 'POST',
            body: {
                email: email.value,
                password: password.value
            }
        })
        
        // ✨ 修正：登入成功後才設定 loggedIn.value 為 true
        loggedIn.value = true 
        
        // 儲存使用者資訊到 localStorage
        if (process.client) {
            // ... (儲存 user 資訊)
             localStorage.setItem('user', JSON.stringify({
                 id: res.id,
                 username: res.username,
                 email: res.email,
                 hotel_id: res.hotel_id
             }))
        }
        
        success.value = res.message || '登入成功！'
        
        // 延遲後導向首頁
        setTimeout(() => {
            router.push('/')
        }, 800)
        
    } catch (e) {
        console.error('Login error:', e)
        const message = e?.data?.detail || '登入失敗，請檢查帳號密碼'
        error.value = Array.isArray(message) ? message.join(', ') : message
        // 登入失敗時，loggedIn 保持為 false (初始值) 或明確設定為 false
        loggedIn.value = false // 確保狀態正確
    } finally {
        loading.value = false
    }
}
</script>
