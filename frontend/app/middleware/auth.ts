import { useUser } from '~/composables/useAuth';

export default defineNuxtRouteMiddleware(async (to, from) => {
    // 🚩 修正 2 & 3：加上 "as any"
    // 告訴 TypeScript：「別管它是不是 null 了，把它當成任意物件處理！」
    // 這樣 user.value = data 才塞得進去，user.value.role 才讀得到
    const user = useUser() as any; 

    // 1. 如果 user 狀態是空的，嘗試呼叫一次 /auth/me 確認身分
    if (!user.value) {
        try {
            const config = useRuntimeConfig();
            
            // 🚩 修正 1：改用 "import.meta.server"
            // Nuxt 3 / Vite 推薦用這個來取代 process.server，這樣就不會報錯說找不到 process 了
            const apiBase = import.meta.server 
                ? 'http://host.docker.internal:8000' 
                : config.public.apiBase;

            // 轉發 Cookie (SSR 必要)
            const headers = useRequestHeaders(['cookie']);
            
            const data = await $fetch(`${apiBase}/auth/me`, {
                headers: headers
            });
            
            if (data) user.value = data;
        } catch (e) {
            user.value = null;
        }
    }

    // 2. 判斷邏輯
    const isLoggedIn = !!user.value;
    const publicPages = ['/login', '/register', '/registerOwner'];
    const isPublicPage = publicPages.includes(to.path);

    // 未登入 -> 去登入頁
    if (!isLoggedIn && !isPublicPage) {
        return navigateTo('/login');
    }

    // 已登入 -> 踢回首頁或管理頁
    if (isLoggedIn && isPublicPage) {
        // 因為上面加了 as any，這裡使用 ?. 就不會報錯了
        if (user.value?.role === 'owner') {
            return navigateTo('/settingHotel');
        }
        return navigateTo('/');
    }
});