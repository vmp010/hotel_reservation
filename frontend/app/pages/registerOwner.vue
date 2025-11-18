<template>
  <div class="d-flex justify-content-center align-items-center vh-100 bg-light">
    <div class="card p-4 shadow" style="width: 400px;">
      <h3 class="text-center mb-4 text-primary">業主註冊帳號</h3>
      <form @submit.prevent="handleregister">
        <div class="mb-3">
          <label class="form-label">業者名稱</label>
          <input v-model="ownerName" type="text" class="form-control" placeholder="輸入業者名稱" required>
        </div>
        <div class="mb-3">
          <label class="form-label">電子郵件</label>
          
          <input v-model="email" type="gmail" class="form-control" placeholder="輸入 Email" required>
        </div>
        
        <div class="mb-3">
          <label class="form-label">密碼</label>
          <input v-model="password" type="password" class="form-control" placeholder="輸入密碼" required>
        </div>
        <div class="mb-3">
          <label class="form-label">確認密碼</label>
          <input v-model="confirm_password" type="password" class="form-control" placeholder="再次輸入密碼" required>
        </div>
        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          {{ loading ? '註冊中...' : '註冊' }}
        </button>
        <p v-if="error" class="text-danger mt-2">{{ error }}</p>
        <p v-if="success" class="text-success mt-2">{{ success }}</p>
      </form>
      <p class="text-center mt-3">
        已經有業主帳號了？<NuxtLink to="/hotelierLogin">業主登入</NuxtLink>
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
const ownerName = ref('')
const password = ref('')
const confirm_password = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const handleregister = async () => {
  error.value = ''
  success.value = ''
  if (password.value !== confirm_password.value) {
    error.value = '兩次密碼不一致'
    return
  }
  loading.value = true
  try {
    const res = await $fetch(`${config.public.apiBase}/auth/register/owner`, {
      method: 'POST',
      body: {
        email: email.value,
        owner_name: ownerName.value,
        password: password.value
      }
    })
    success.value = '註冊成功，將導向登入頁面'
    setTimeout(() => router.push('/hotelierLogin'), 800)
  } catch (e) {
    const message = e?.data?.detail || '註冊失敗，請稍後再試'
    error.value = Array.isArray(message) ? message.join(', ') : message
  } finally {
    loading.value = false
  }
}
</script>
