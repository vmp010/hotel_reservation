# Alembic 設定變更記錄

本文件記錄了設定 Alembic 資料庫遷移系統所做的所有變更。

---

## 📝 修改的檔案清單

### 1. `backend/requirements.txt`
**變更**：新增 Alembic 套件
```diff
+ alembic==1.13.1
```

### 2. `backend/main.py`
**變更**：註解掉自動建立表格的程式碼
```diff
- models.Base.metadata.create_all(bind=engine)
+ # 註解掉 create_all，改用 Alembic 管理資料庫結構
+ # models.Base.metadata.create_all(bind=engine)
```

### 3. `backend/alembic/env.py`
**變更**：完整重寫，加入 models 連接和環境變數支援
```python
# 主要變更：
- target_metadata = None
+ import models
+ from database import Base
+ target_metadata = Base.metadata

+ # 從環境變數讀取資料庫 URL
+ database_url = os.getenv("DATABASE_URL", "...")
+ config.set_main_option("sqlalchemy.url", database_url)
```

### 4. `backend/alembic.ini`
**變更**：更新資料庫 URL 預設值
```diff
- sqlalchemy.url = ${DATABASE_URL}
+ sqlalchemy.url = mysql+pymysql://admin:admin123@localhost:3307/hotel_reservation
```

### 5. `docker-compose.yml`
**變更**：backend 服務加入健康檢查依賴
```diff
  backend:
    depends_on:
-     - db
+     db:
+       condition: service_healthy
+   restart: on-failure
```

### 6. `backend/alembic/versions/443b2fa7efe5_initial_tables.py`
**變更**：初始遷移檔（新增檔案）
- 建立 `users` 表格
- 建立 `hotel_rooms` 表格
- 移除了自動產生的外鍵約束

---

## 📄 新增的文件

### 1. `backend/MIGRATION_GUIDE.md`
- 詳細的 Alembic 使用說明
- 範例流程
- 故障排除

### 2. `ALEMBIC_SETUP.md`
- 完整的設定指南
- 新成員上手流程
- 團隊協作最佳實踐

### 3. `README.md`
- 更新專案說明
- 加入 Alembic 使用說明
- 服務端口列表
- 故障排除

### 4. `QUICKSTART.md`
- 快速指令參考
- 常用操作清單

### 5. `ALEMBIC_CHANGES.md`（本檔案）
- 記錄所有變更

---

## 🔄 套用變更的步驟

### 對於已經 Clone 專案的成員：

```powershell
# 1. 拉取最新程式碼
git pull

# 2. 停止現有容器
docker compose down

# 3. （可選）刪除舊資料庫（會清空資料）
docker volume rm hotel_reservation_db_data

# 4. 重建並啟動容器
docker compose up -d --build

# 5. 套用資料庫遷移
docker exec -it hotel_backend alembic upgrade head

# 6. 驗證
docker exec -it hotel_backend alembic current
# 應該顯示：443b2fa7efe5 (head)
```

### 對於新成員：

```powershell
# 1. Clone 專案
git clone https://github.com/vmp010/hotel_reservation.git
cd hotel_reservation

# 2. 啟動所有服務
docker compose up -d --build

# 3. 套用資料庫遷移
docker exec -it hotel_backend alembic upgrade head
```

---

## ✅ 驗證檢查清單

完成設定後，請確認：

- [ ] 所有容器正常運行：`docker ps`
- [ ] 後端服務正常：http://localhost:8000
- [ ] 前端服務正常：http://localhost:3000
- [ ] Alembic 版本正確：`docker exec -it hotel_backend alembic current`
- [ ] 資料表已建立：
  - [ ] 在 phpMyAdmin (http://localhost:8080) 看到 `users` 表
  - [ ] 在 phpMyAdmin 看到 `hotel_rooms` 表
  - [ ] 在 phpMyAdmin 看到 `alembic_version` 表

---

## 🎯 核心優點

### 之前（使用 create_all）：
❌ 無法追蹤資料庫變更歷史  
❌ 修改 model 後需要手動更新資料庫  
❌ 團隊成員資料庫結構可能不一致  
❌ 無法輕鬆回溯到舊版本  
❌ 新欄位加入後舊資料會遺失  

### 現在（使用 Alembic）：
✅ 完整的版本控制  
✅ 自動偵測 model 變更  
✅ 團隊成員資料庫一致  
✅ 可以升級/降級版本  
✅ 保留現有資料  
✅ 支援複雜的資料遷移  

---

## 📞 問題回報

如果在設定過程中遇到問題：

1. 查看 [ALEMBIC_SETUP.md](ALEMBIC_SETUP.md) 的故障排除章節
2. 檢查容器日誌：`docker logs hotel_backend`
3. 在 GitHub 開 Issue：https://github.com/vmp010/hotel_reservation/issues

---

**設定日期**：2025-10-29  
**負責人**：vmp010  
**Alembic 版本**：1.13.1
