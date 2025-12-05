// import { useAuthToken, handle401Error } from '~/composables/useAuth'; 

// export default defineNuxtPlugin(nuxtApp => {
//     const authToken = useAuthToken();

//     globalThis.$fetch = $fetch.create({
//         onRequest({ options }) {
//             // 🔍 加入這行 Log 來除錯
//             console.log('🚨 全域攔截器啟動！目前的 Token:', authToken.value);

//             if (authToken.value) {
//                 options.headers = options.headers || {};
//                 options.headers.Authorization = `Bearer ${authToken.value}`;
//                 // 🔍 確認 Header 有被加入
//                 console.log('✅ Header 已加入:', options.headers.Authorization);
//             } else {
//                 console.warn('⚠️ 攔截器發現 Token 為空，未加入 Header');
//             }
//         },
//         onResponseError({ response }) {
//             if (response.status === 401) {
//                 console.error('API 響應 401: Token 無效或過期');
//             }
//         }
//     });
// });