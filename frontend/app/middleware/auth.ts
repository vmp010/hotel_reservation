import { useUser } from '~/composables/useAuth';

export default defineNuxtRouteMiddleware(async (to, from) => {
    // 解決錯誤 1：告訴 TS 這個 user 可以是任何型別
    const user = useUser() as any; 

    // 1. 如果 user 狀態是空的，嘗試呼叫一次 /auth/me 確認身分
    if (!user.value) {
        try {
            const config = useRuntimeConfig();
            const headers = useRequestHeaders(['cookie']);
            
            // 這裡使用 $fetch 取得資料
            const data = await $fetch(`${config.public.apiBase}/auth/me`, {
                headers: headers
            });
            
            if (data) {
                user.value = data;
            }
        } catch (e) {
            user.value = null;
        }
    }

    const isLoggedIn = !!user.value;

    // A. 未登入邏輯
    const publicPages = ['/login', '/register', '/registerOwner'];
    const isPublicPage = publicPages.includes(to.path);

    if (!isLoggedIn && !isPublicPage) {
        return navigateTo('/login');
    }

    // B. 已登入邏輯
    if (isLoggedIn && isPublicPage) {
        // 解決錯誤 2：加上 ?. 防止 user.value 為 null 時報錯
        if (user.value?.role === 'owner') {
            return navigateTo('/settingHotel');
        }
        return navigateTo('/');
    }
});