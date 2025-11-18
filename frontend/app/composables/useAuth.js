import { useState, useCookie } from '#app';
import {computed} from 'vue'
import { useRouter } from 'vue-router'; // 引入 useRouter 供登出時使用

// 1. 儲存使用者資料 (用於個人中心頁面)
export const useUser = () => useState('user', () => null);

// 2. 儲存 JWT Token (使用 useCookie 確保跨頁面和 SSR/CSR 持久化)
export const useAuthToken = () => useCookie('auth_token', {
    maxAge: 60 * 60 * 24 * 7, // 7 天有效期
    sameSite: 'lax',
    // httpOnly 應由後端設定，這裡只處理前端存取
});

// 3. 登入狀態 (只要有 Token 就視為已登入)
export const useLoggedIn = () => {
    const authToken = useAuthToken();
    return computed(() => !!authToken.value);
};

// 4. 核心登出清理邏輯
export const performLogoutCleanup = () => {
    const user = useUser();
    const authToken = useAuthToken();
    const loggedIn = useLoggedIn(); // 雖然是 computed，但這裡也獲取以確保邏輯完整

    // 清理狀態
    user.value = null;
    authToken.value = null; // 清除 Cookie
    loggedIn.value = false; // 雖然會被 computed 覆蓋，但確保邏輯流暢

    // 清除 localStorage 中儲存的 user 資訊 (登入頁面的邏輯)
    if (process.client) {
        localStorage.removeItem('user');
    }

    console.log('✅ 登出清理完成：JWT/Cookie/localStorage 已清除。');
};

// 5. [可選] JWT 驗證失敗時的通用登出流程
export const handle401Error = async () => {
    const router = useRouter();
    performLogoutCleanup();
    // 導航到登入頁面
    await router.push('/login');
    // 可以添加通知，例如：Swal.fire('會話過期', '請重新登入。', 'error');
};