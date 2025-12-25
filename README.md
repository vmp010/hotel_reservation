# Hotel Reservation

這是一個使用 **FastAPI** (後端) 和 **Nuxt.js** (前端) 建立的訂房網站專案。

---

## ✨ 更新重點
- 專案目前使用 **SQLite** 作為資料庫，並透過 `coleifer/sqlite-web` 提供網頁介面（預設在 http://localhost:8081）。
- 使用 Docker Compose 管理三個主要服務：**backend**（FastAPI）、**frontend**（Nuxt）與 **sqlite-web**（資料庫 UI）。

---

## 🚀 快速開始

### 第一次啟動
```bash
# 1. Clone 專案
git clone https://github.com/vmp010/hotel_reservation.git
cd hotel_reservation

# 2. 啟動所有服務
docker compose up -d --build

# 3. 套用資料庫遷移
docker exec -it hotel_backend alembic upgrade head
```

### 後續啟動
```bash
docker compose up -d
```

---

## 📦 服務端口

| 服務 | 端口 | 說明 |
|------|------|------|
| Frontend (Nuxt) | http://localhost:3000 | 前端網頁 |
| Backend (FastAPI) | http://localhost:8000 | API 後端 |
| API Docs (Swagger) | http://localhost:8000/docs | 自動產生的 API 文件 |
| sqlite-web (DB UI) | http://localhost:8081 | SQLite 資料庫管理介面 |

**資料庫（容器內）路徑**：`/data/hotel_reservation.db`（掛載至本機卷 `sqlite-data`）



## 📁 專案結構

```
hotel_reservation/
├── backend/                 # FastAPI 後端
│   ├── main.py             # FastAPI 應用主程式
│   ├── models.py           # SQLAlchemy 資料模型
│   ├── database.py         # 資料庫連線設定
│   ├── requirements.txt    # Python 套件清單
│   ├── alembic/            # 資料庫遷移檔
│   │   └── versions/       # 遷移版本記錄
│   └── dockerfile          # 後端 Docker 映像
├── frontend/               # Nuxt.js 前端
│   ├── app/
│   │   ├── pages/          # 頁面路由
│   │   └── components/     # Vue 組件
│   ├── nuxt.config.ts      # Nuxt 設定
│   ├── package.json        # Node 套件清單
│   └── dockerfile          # 前端 Docker 映像
├── docker-compose.yml      # Docker Compose 設定
├── README.md               # 本檔案
└── ALEMBIC_SETUP.md        # Alembic 詳細說明
```

---

## 🛠️ 開發指令

### 查看容器日誌
```bash
# 查看所有服務
docker compose logs -f

# 查看特定服務
docker compose logs -f backend
docker compose logs -f frontend
```

### 重啟服務
```bash
# 重啟所有服務
docker compose restart

# 重啟特定服務
docker compose restart backend
docker compose restart frontend
```

### 停止服務
```bash
docker compose down
```

### 重建容器（程式碼或套件更新後）
```bash
docker compose up -d --build
```

---


## 📝 功能特點

### 後端 (FastAPI)
- ✅ 使用者註冊（密碼 bcrypt 加密）
- ✅ RESTful API 設計
- ✅ 自動生成 API 文件（Swagger UI）
- ✅ SQLAlchemy ORM
- ✅ Alembic 資料庫遷移
- ✅ CORS 跨域設定

### 前端 (Nuxt.js)
- ✅ 響應式設計（Bootstrap）
- ✅ 註冊頁面
- ✅ 表單驗證
- ✅ 錯誤處理與使用者提示

---

## 🔌 主要功能與 API（快速概要）

- 身份驗證與權限
  - POST `/auth/register/user` - 使用者註冊
  - POST `/auth/register/owner` - 店家註冊
  - POST `/auth/token` - 使用者/店家登入（回傳 cookie)
  - POST `/auth/logout` - 登出
  - GET `/auth/me` - 取得當前登入資訊

- 飯店相關
  - GET `/hotels/search/` - 搜尋可預訂的飯店（含日期與地點篩選）
  - POST `/hotels/create` - 店家建立飯店
  - PATCH `/hotels/edit/{hotel_id}` - 編輯飯店
  - DELETE `/hotels/delete/{hotel_id}` - 下架飯店
  - GET `/hotels/my_hotels` - 店家取得自己的飯店列表

- 訂單 / 購物車
  - POST `/bookings/create` - 建立訂單（立即付款）
  - GET `/bookings/unavailable_dates/{hotel_id}` - 取得該飯店已被預訂的日期
  - POST `/carts/add/{hotel_id}` - 加入購物車（CART）
  - POST `/carts/checkout` - 結帳（CART -> PAID）
  - GET `/carts/` - 取得購物車項目

- 評論
  - POST `/reviews/create` - 新增評論（需為該筆訂單的使用者）
  - GET `/reviews/{hotel_id}` - 取得某飯店的所有評論
  - PUT `/reviews/{review_id}` - 更新評論（僅作者）
  - DELETE `/reviews/delete/{review_id}` - 刪除評論（僅作者）

> 詳細 API 請參見 Swagger：`http://localhost:8000/docs`

---


*


