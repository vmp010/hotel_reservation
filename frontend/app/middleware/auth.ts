export default defineNuxtRouteMiddleware((to, from) => {
  // 模擬「是否登入」
  const isLoggedIn = useState('loggedIn').value

  if (!isLoggedIn) {
    // 沒登入 → 轉跳到登入頁
    return navigateTo('/login')
  }
})