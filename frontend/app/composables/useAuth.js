//引入Nuxt 內建的狀態管理工具
import {useState,useCookie} from '#app'

//1. 定義並導出登入狀態(true/false)
// 導航列跟登入頁面使用的狀態
export const useLoggedIn = () => useState('loggedIn',() =>false)

// 2. 定義並導出 Token 狀態 (用於清理)
// 即使您目前還沒用，先定義好以便清理
export const useAuthToken = () => useCookie('auth_token');

// 3. 核心登出請理邏輯
export const performLogoutCleanup = () =>{
    //取得所有需要清理的狀態
    const loggedIn = useLoggedIn();
    const authToken = useAuthToken();

    //清理狀態
    loggedIn.value = false;
    authToken.value = null;

    //清除 localStorage 中儲存的user資訊(登入頁面的邏輯)
    if(process.client){
        localStorage.removeItem('user');
    }

    console.log('登出清理完成：loggedIn設定為 false,Token和localStorage以清除');
};