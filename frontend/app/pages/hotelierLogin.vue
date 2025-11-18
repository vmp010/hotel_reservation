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
        還沒有帳號？<NuxtLink to="/registerOwner">註冊(這邊應該要改成業者的api)</NuxtLink>
      </p>
    </div>
  </div>
</template>

<script setup>

</script>
