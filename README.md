# Hotel Reservation

這是一個使用 **FastAPI** (後端) 和 **Nuxt.js** (前端) 建立的訂房網站專案。

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
| API Docs | http://localhost:8000/docs | Swagger API 文件 |
| phpMyAdmin | http://localhost:8080 | 資料庫管理介面 |
| MySQL | localhost:3307 | 資料庫 (外部連線) |

**資料庫連線資訊**：
- 主機：`db` (容器內) 或 `localhost:3307` (外部)
- 使用者：`admin`
- 密碼：`admin123`
- 資料庫名稱：`hotel_reservation`

---

## 🗄️ 資料庫遷移 (Alembic)

本專案使用 Alembic 進行資料庫版本控制。

### 首次設定（新成員）
```bash
docker exec -it hotel_backend alembic upgrade head
```

### 修改資料庫結構
1. 修改 `backend/models.py`
2. 產生遷移：
   ```bash
   docker exec -it hotel_backend alembic revision --autogenerate -m "描述變更"
   ```
3. 套用遷移：
   ```bash
   docker exec -it hotel_backend alembic upgrade head
   ```
4. 提交變更：
   ```bash
   git add backend/models.py backend/alembic/versions/*.py
   git commit -m "Database: 描述變更"
   git push
   ```

### 同步他人的資料庫變更
```bash
git pull
docker compose restart backend
docker exec -it hotel_backend alembic upgrade head
```

**詳細說明**：查看 [ALEMBIC_SETUP.md](ALEMBIC_SETUP.md)

---

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

## 🔧 故障排除

### 問題：前端無法連接後端
**檢查**：
1. 確認後端容器運行：`docker ps`
2. 檢查後端日誌：`docker logs hotel_backend`
3. 確認 CORS 設定正確（`backend/main.py` 的 origins）

### 問題：資料庫連線失敗
**解決**：
```bash
# 重啟資料庫
docker compose restart db

# 等待健康檢查通過，然後重啟後端
docker compose restart backend
```

### 問題：資料表不存在
**解決**：
```bash
# 套用所有遷移
docker exec -it hotel_backend alembic upgrade head
```

### 問題：完全重置（開發環境）
```bash
docker compose down
docker volume rm hotel_reservation_db_data
docker compose up -d --build
docker exec -it hotel_backend alembic upgrade head
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

## 🤝 貢獻指南

1. Fork 本專案
2. 建立功能分支：`git checkout -b feature/new-feature`
3. 提交變更：`git commit -m "Add new feature"`
4. 推送到分支：`git push origin feature/new-feature`
5. 建立 Pull Request

**資料庫變更**：請務必使用 Alembic 遷移，參考 [ALEMBIC_SETUP.md](ALEMBIC_SETUP.md)

---

## 📄 授權

MIT License

---

## 👥 維護者

[@vmp010](https://github.com/vmp010)


