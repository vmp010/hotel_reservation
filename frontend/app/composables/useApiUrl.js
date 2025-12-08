// composables/useApiUrl.js

export const useApiUrl = () => {
    // 1. 如果是在 Docker 伺服器端 (SSR) 執行
    // 必須連線到 Docker 內部的網路名稱
    if (process.server) {
        return 'http://host.docker.internal:8000';
    }

    // 2. 如果是在使用者的瀏覽器端 (Client) 執行
    // window.location.hostname 會自動抓取 'localhost' 或 '127.0.0.1'
    // 這樣就不用寫死，會自動跟著變！
    return `http://${window.location.hostname}:8000`;
};