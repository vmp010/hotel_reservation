import { useState, useCookie } from '#app';
import {computed} from 'vue'
import { useRouter } from 'vue-router'; // 引入 useRouter 供登出時使用

// 1. 儲存使用者資料 (用於個人中心頁面)
export const useUser = () => useState('user', () => null);

// 2. 儲存 JWT Token 
export const useAuthToken = () => useCookie('auth_token', {
    maxAge: 60 * 60 * 24 * 7, // 7 天有效期
    sameSite: 'lax',
});

// 3. 登入狀態 (只要有 Token 就視為已登入)
export const useLoggedIn = () => {
    const authToken = useAuthToken();
    return computed(() => !!authToken.value);
};

// 4. 核心登出清理邏輯 (保持不變)
export const performLogoutCleanup = () => {
    const user = useUser();
    const authToken = useAuthToken();
    
    user.value = null;
    authToken.value = null;

    if (process.client) {
        localStorage.removeItem('user');
    }
    console.log('✅ 登出清理完成：JWT/Cookie/localStorage 已清除。');
};


// 5. 應用程式啟動時的初始化函式 (恢復使用者狀態)
export const initializeUserSession = async () => {
    const authToken = useAuthToken();
    const user = useUser();
    
    // 如果全域狀態中已經有資料了 (例如，剛登入或已經被初始化過)，則不需重複執行
    if (user.value) {
        return;
    }

    // 檢查是否有 Token
    if (authToken.value) {
        // 🚩 核心邏輯：嘗試從 localStorage 恢復使用者資訊
        if (process.client) {
            const storedUser = localStorage.getItem('user');
            if (storedUser) {
                try {
                    // 將 localStorage 的備份資料恢復到全域狀態
                    user.value = JSON.parse(storedUser);
                    console.log('✅ 用戶資料從 localStorage 恢復成功。');
                    return;
                } catch (e) {
                    console.error('從 localStorage 恢復用戶資料失敗', e);
                    performLogoutCleanup(); // 恢復失敗，強制登出
                }
            }
        }
        
        // 🚨 未來：如果 localStorage 沒有資料，這裡將會調用 /users/me API 來獲取最新資料。
        // else {
        //   await $fetch('/users/me', { headers: { Authorization: `Bearer ${authToken.value}` } });
        // }
    }
};

// 6. [可選] JWT 驗證失敗時的通用登出流程 (保持不變)
export const handle401Error = async () => {
    const router = useRouter();
    performLogoutCleanup();
    await router.push('/login');
};