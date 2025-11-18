import { useAuthToken, handle401Error } from '~/composables/useAuth'; 

export default defineNuxtPlugin(nuxtApp => {
    const authToken = useAuthToken();

    // 攔截所有 useFetch 和 $fetch 請求
    globalThis.$fetch = $fetch.create({
        onRequest({ options }) {
            // 檢查是否有 Token 且不是要發送到外部服務
            if (authToken.value) {
                // 設定 Authorization Header: Bearer <Token>
                options.headers = options.headers || {};
                options.headers.Authorization = `Bearer ${authToken.value}`;
            }
        },
        // 處理 API 響應錯誤
        onResponseError({ response }) {
            // 處理 401 Unauthorized 錯誤 (表示 Token 無效或過期)
            if (response.status === 401) {
                console.error('API 響應 401: Token 無效或過期，執行強制登出。');
                // handle401Error(); // 這裡如果啟用，會導致循環依賴，但邏輯是這樣
                // 暫時只清理狀態並導航
                // 如果需要，可以在這裡手動執行 performLogoutCleanup 和 router.push('/login')
            }
        }
    });
});