# 快速指令清單

## 🚀 新成員快速設定（3 步驟）

```powershell
# 1. Clone 並啟動
git clone https://github.com/vmp010/hotel_reservation.git
cd hotel_reservation
docker compose up -d --build

# 2. 套用資料庫遷移
docker exec -it hotel_backend alembic upgrade head

# 3. 驗證
# 開啟 http://localhost:3000 (前端)
# 開啟 http://localhost:8000/docs (API 文件)
# 開啟 http://localhost:8080 (phpMyAdmin)
```

---

## 📝 日常開發指令

### 修改資料庫結構
```powershell
# 1. 修改 backend/models.py
# 2. 產生遷移
docker exec -it hotel_backend alembic revision --autogenerate -m "add new column"

# 3. 套用遷移
docker exec -it hotel_backend alembic upgrade head

# 4. 提交
git add backend/models.py backend/alembic/versions/*.py
git commit -m "Database: add new column"
git push
```

### 同步他人的變更
```powershell
git pull
docker compose restart backend
docker exec -it hotel_backend alembic upgrade head
```

### 查看資料庫狀態
```powershell
# 當前版本
docker exec -it hotel_backend alembic current

# 遷移歷史
docker exec -it hotel_backend alembic history
```

---

## 🔄 容器管理

```powershell
# 啟動所有服務
docker compose up -d

# 重啟特定服務
docker compose restart backend

# 查看日誌
docker logs hotel_backend -f

# 停止所有服務
docker compose down

# 重建（套件更新後）
docker compose up -d --build
```

---

## 🗄️ 資料庫管理

```powershell
# 進入資料庫容器
docker exec -it hotel_db mysql -u admin -padmin123 hotel_reservation

# 備份資料庫
docker exec hotel_db mysqldump -u admin -padmin123 hotel_reservation > backup.sql

# 還原資料庫
docker exec -i hotel_db mysql -u admin -padmin123 hotel_reservation < backup.sql
```

---

## ⚠️ 緊急重置（開發環境，會刪除所有資料）

```powershell
docker compose down
docker volume rm hotel_reservation_db_data
docker compose up -d --build
docker exec -it hotel_backend alembic upgrade head
```

---

## 📚 詳細文件

- 完整 README：[README.md](README.md)
- Alembic 設定：[ALEMBIC_SETUP.md](ALEMBIC_SETUP.md)
- 遷移指南：[backend/MIGRATION_GUIDE.md](backend/MIGRATION_GUIDE.md)
