import { useState, useCookie } from '#app';
import {computed} from 'vue';
import { useRouter } from 'vue-router'; 
import { jwtDecode } from 'jwt-decode'; // 🚨 確保已安裝此套件

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

// 4. 核心登出清理邏輯
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
    
    // 如果全域狀態中已經有資料了，則不需重複執行
    if (user.value) { return; }

    // 檢查是否有 Token
    if (authToken.value) {
        
        // 🚩 核心修正：直接從 JWT Token 解析
        try {
            const token = authToken.value;
            const decodedPayload = jwtDecode(token); // 解析 Token
            
            // 🚨 修正：構造完整的 user 物件，使用 Token Payload 中的 ID/sub
            const decodedId = decodedPayload.id || decodedPayload.user_id || decodedPayload.owner_id;
            
            user.value = {
                id: decodedId, 
                username: decodedPayload.sub || '未知用戶',
                email: decodedPayload.email || '未知信箱',
                role: decodedPayload.role || 'user',
                // 這裡可以加入更多您需要的欄位
            };
            
            // 🚨 僅在客戶端，將完整的 user 物件寫入 localStorage 備份 (供下一次恢復)
            if (process.client) {
                localStorage.setItem('user', JSON.stringify(user.value));
            }
            
            console.log('✅ 用戶資料從 JWT Payload 恢復成功。ID:', user.value.id);
            
        } catch (e) {
            console.error('從 JWT 解析或恢復用戶資料失敗，執行登出。', e);
            performLogoutCleanup(); // 解析失敗，強制登出
        }
    }
};

// 6. [可選] JWT 驗證失敗時的通用登出流程 (保持不變)
export const handle401Error = async () => {
    const router = useRouter();
    performLogoutCleanup();
    await router.push('/login');
};