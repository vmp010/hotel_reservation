import { useState } from '#app';
import { computed } from 'vue';
import { useRouter } from 'vue-router';

// 1. 儲存使用者資料 (全域狀態)
export const useUser = () => useState('user', () => null);

// 2. 登入狀態 (只要 user 有資料就視為已登入)
export const useLoggedIn = () => {
    const user = useUser();
    return computed(() => !!user.value);
};

// 3. 核心登出清理邏輯
// 現在需要呼叫後端 API 來清除 HttpOnly Cookie
export const performLogoutCleanup = async () => {
    const user = useUser();
    const config = useRuntimeConfig();
    const router = useRouter();

    try {
        // 呼叫後端清除 Cookie
        await $fetch(`${config.public.apiBase}/auth/logout`, {
            method: 'POST'
        });
    } catch (e) {
        console.error('登出 API 呼叫失敗 (可能 Token 已過期)', e);
    } finally {
        // 不管後端成不成功，前端都要清除狀態並跳轉
        user.value = null;
        if (process.client) {
            window.location.href = '/'; // 強制刷新回首頁
        }
    }
    console.log('✅ 登出清理完成。');
};

// 4. 應用程式啟動時的初始化函式 (恢復使用者狀態)
// 🚀 關鍵修改：不再解碼 Token，而是呼叫 /auth/me API
export const initializeUserSession = async () => {
    const user = useUser();
    const config = useRuntimeConfig();

    // 如果全域狀態中已經有資料了，則不需重複執行
    if (user.value) return;

    try {
        // 發送請求給後端，瀏覽器會自動帶上 HttpOnly Cookie
        // 這裡需要後端有一支 GET /auth/me 的 API
        const data = await $fetch(`${config.public.apiBase}/auth/me`, {
            retry: 0, // 不需要重試，失敗就代表沒登入
            // 🚨 強制瀏覽器攜帶 Cookie (憑證)
            credentials: 'include'
        });

        if (data) {
            // 後端回傳的資料結構應該包含 id, username, role, email
            user.value = {
                id: data.id,
                username: data.username || data.owner_name, // 兼容 owner 和 user
                email: data.email,
                role: data.role
            };
            console.log('✅ 使用者狀態已從後端恢復:', user.value.role);
        }
    } catch (e) {
        // 401 代表沒登入或 Token 過期，這是正常現象，清空狀態即可
        user.value = null;
        if (e.response?.status !== 401) {
            console.error('恢復使用者狀態失敗:', e);
        }
    }
};

// 5. [可選] JWT 驗證失敗時的通用登出流程
export const handle401Error = async () => {
    const router = useRouter();
    await performLogoutCleanup();
};

// ❌ 已移除：useAuthToken (因為前端讀不到 HttpOnly Cookie 了)
// export const useAuthToken = ...