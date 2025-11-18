import { useAuthToken } from '~/composables/useAuth'; // 確保路徑正確

export default defineNuxtRouteMiddleware((to, from) => {
    // 取得儲存在 Cookie 裡的 JWT Token
    const authToken = useAuthToken();

    // 🚩 判斷邏輯：只要 authToken.value 存在且非空，就視為已登入
    if (!authToken.value) {
        // 如果沒有 Token (未登入)
        if (to.path !== '/login' && to.path !== '/register') {
            // 避免無限重定向
            return navigateTo('/login');
        }
    }
    
    // 如果已登入，且試圖訪問 /login 頁面，則導航到首頁
    if (authToken.value && (to.path === '/login' || to.path === '/register')) {
        return navigateTo('/');
    }
});