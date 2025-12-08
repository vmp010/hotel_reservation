import { useUser } from '~/composables/useAuth';
// Nuxt 會自動引入 useApiUrl，不需要手動 import

export default defineNuxtRouteMiddleware(async (to, from) => {
    // 🚩 修正：加上 "as any" 解決 TypeScript 報錯
    const user = useUser() as any; 

    // 1. 如果 user 狀態是空的，嘗試呼叫一次 /auth/me 確認身分
    if (!user.value) {
        try {
            // 🚀 關鍵修改：移除舊的手寫邏輯，改用統一的工具
            // 這樣不管是 SSR (Docker內) 還是 Client (127.0.0.1/localhost) 都會自動對應
            const apiBase = useApiUrl();

            // 轉發 Cookie (SSR 必要)
            const headers = useRequestHeaders(['cookie']);
            
            // 使用動態網址呼叫 API
            const data = await $fetch(`${apiBase}/auth/me`, {
                headers: headers,
                credentials: 'include', // 確保帶上 Cookie
                retry: 0 // 失敗不重試，直接視為未登入
            });
            
            if (data) user.value = data;
        } catch (e) {
            user.value = null;
        }
    }

    // 2. 判斷邏輯 (保持不變)
    const isLoggedIn = !!user.value;
    const publicPages = ['/login', '/register', '/registerOwner'];
    const isPublicPage = publicPages.includes(to.path);

    // 未登入 -> 去登入頁
    if (!isLoggedIn && !isPublicPage) {
        return navigateTo('/login');
    }

    // 已登入 -> 踢回首頁或管理頁
    if (isLoggedIn && isPublicPage) {
        if (user.value?.role === 'owner') {
            return navigateTo('/settingHotel');
        }
        return navigateTo('/');
    }
});