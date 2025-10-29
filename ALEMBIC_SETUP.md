# Alembic 資料庫遷移設定指南

本專案使用 Alembic 進行資料庫版本控制和遷移管理。

---

## 📋 已完成的配置

### 1. 套件安裝
在 `backend/requirements.txt` 已加入：
```
alembic==1.13.1
```

### 2. Alembic 環境配置
`backend/alembic/env.py` 已設定：
- 自動導入 `models.py` 和 `database.py`
- 從環境變數讀取 `DATABASE_URL`
- 連接到 `Base.metadata` 以支援自動偵測變更

### 3. FastAPI 主程式調整
`backend/main.py` 已註解掉：
```python
# models.Base.metadata.create_all(bind=engine)
```
改用 Alembic 管理資料庫結構。

### 4. Docker Compose 優化
`docker-compose.yml` 的 backend 服務已加入健康檢查：
```yaml
depends_on:
  db:
    condition: service_healthy
restart: on-failure
```

---

## 🚀 首次設定流程（新成員加入專案）

### 步驟 1：Clone 專案
```powershell
git clone https://github.com/vmp010/hotel_reservation.git
cd hotel_reservation
```

### 步驟 2：啟動 Docker 容器
```powershell
docker compose up -d --build
```

### 步驟 3：等待容器啟動完成
```powershell
# 檢查容器狀態
docker ps
```
確認所有容器都是 `Up` 狀態。

### 步驟 4：套用資料庫遷移
```powershell
# 檢查當前資料庫版本
docker exec -it hotel_backend alembic current

# 套用所有遷移到最新版本
docker exec -it hotel_backend alembic upgrade head
```

### 步驟 5：驗證
開啟 phpMyAdmin：http://localhost:8080
- 伺服器：`db`
- 使用者：`admin`
- 密碼：`admin123`

應該看到：
- ✅ `users` 表格
- ✅ `hotel_rooms` 表格
- ✅ `alembic_version` 表格（記錄當前版本）

---

## 🔄 修改資料庫結構流程

### 情境：新增欄位到 User 表格

#### 步驟 1：修改 models.py
```python
# backend/models.py
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    hotel_id = Column(Integer)
    phone = Column(String(20), nullable=True)  # 新增欄位
```

#### 步驟 2：產生遷移腳本
```powershell
docker exec -it hotel_backend alembic revision --autogenerate -m "add phone column to users"
```

**說明**：
- `--autogenerate`：自動比對 model 和資料庫差異
- `-m "訊息"`：描述這次變更內容

#### 步驟 3：（可選）檢查產生的遷移檔
```powershell
# 查看最新的遷移檔
ls backend/alembic/versions/
```

#### 步驟 4：套用遷移
```powershell
docker exec -it hotel_backend alembic upgrade head
```

#### 步驟 5：提交到 Git
```powershell
git add backend/models.py
git add backend/alembic/versions/*.py
git commit -m "Add phone column to users table"
git push
```

---

## 🔄 其他成員同步資料庫

當有人推送了新的遷移檔到 GitHub：

### 步驟 1：拉取最新程式碼
```powershell
git pull
```

### 步驟 2：重啟容器（確保程式碼更新）
```powershell
docker compose restart backend
```

### 步驟 3：套用新的遷移
```powershell
docker exec -it hotel_backend alembic upgrade head
```

---

## 📝 常用指令

### 查看資料庫當前版本
```powershell
docker exec -it hotel_backend alembic current
```

### 查看遷移歷史
```powershell
docker exec -it hotel_backend alembic history --verbose
```

### 產生新遷移（自動偵測變更）
```powershell
docker exec -it hotel_backend alembic revision --autogenerate -m "描述變更內容"
```

### 套用所有遷移
```powershell
docker exec -it hotel_backend alembic upgrade head
```

### 回溯到上一個版本
```powershell
docker exec -it hotel_backend alembic downgrade -1
```

### 回溯到特定版本
```powershell
docker exec -it hotel_backend alembic downgrade <revision_id>
```

### 查看下一次升級會執行什麼
```powershell
docker exec -it hotel_backend alembic upgrade head --sql
```

---

## ⚠️ 注意事項

### 1. 不要手動修改資料庫結構
- ❌ 不要在 phpMyAdmin 手動新增/修改欄位
- ✅ 只透過修改 `models.py` + Alembic 遷移

### 2. 檢查自動產生的遷移腳本
Alembic 自動產生的遷移可能不完美，建議：
- 檢查 `backend/alembic/versions/` 裡的新檔案
- 確認 `upgrade()` 和 `downgrade()` 函數正確
- 特別注意：
  - 刪除欄位（會遺失資料）
  - 修改欄位類型（可能需要資料轉換）
  - 外鍵約束（確認關聯正確）

### 3. 團隊協作最佳實踐
- 🔒 **修改 model 前先 pull**：避免遷移衝突
- 📝 **清楚的 commit 訊息**：描述資料庫變更
- 🧪 **本地測試遷移**：確認 upgrade 和 downgrade 都能運作
- 💾 **生產環境先備份**：重要！

### 4. 遷移衝突處理
如果兩個人同時建立遷移，可能會衝突：

```powershell
# 查看當前狀態
docker exec -it hotel_backend alembic current

# 如果有問題，重置到正確的版本
docker exec -it hotel_backend alembic stamp <revision_id>

# 然後重新套用
docker exec -it hotel_backend alembic upgrade head
```

---

## 🔧 故障排除

### 問題 1：容器啟動時資料庫連線失敗
**原因**：後端容器啟動太快，資料庫還沒準備好

**解決**：已在 `docker-compose.yml` 設定健康檢查：
```yaml
depends_on:
  db:
    condition: service_healthy
```

### 問題 2：Alembic 沒有偵測到變更
**檢查清單**：
1. 確認 `models.py` 的 class 有繼承 `Base`
2. 確認 `__tablename__` 正確
3. 確認 `alembic/env.py` 有 `import models`
4. 重啟容器：`docker compose restart backend`

**手動產生空遷移檔**：
```powershell
docker exec -it hotel_backend alembic revision -m "manual migration"
# 然後手動編輯產生的檔案
```

### 問題 3：遷移執行失敗
**檢查**：
```powershell
# 查看詳細錯誤
docker logs hotel_backend

# 檢查資料庫狀態
docker exec -it hotel_backend alembic current
```

**強制標記為特定版本**（謹慎使用）：
```powershell
docker exec -it hotel_backend alembic stamp head
```

### 問題 4：想要完全重置資料庫
**開發環境**（會刪除所有資料）：
```powershell
docker compose down
docker volume rm hotel_reservation_db_data
docker compose up -d
docker exec -it hotel_backend alembic upgrade head
```

**生產環境**：❌ 不要這樣做！使用正確的遷移流程。

---

## 📚 更多資訊

- 完整用法指南：`backend/MIGRATION_GUIDE.md`
- Alembic 官方文件：https://alembic.sqlalchemy.org/
- SQLAlchemy 官方文件：https://docs.sqlalchemy.org/

---

## 🎯 快速參考

### 新成員加入
```powershell
git clone <repo>
cd hotel_reservation
docker compose up -d --build
docker exec -it hotel_backend alembic upgrade head
```

### 修改資料庫
```powershell
# 1. 修改 backend/models.py
# 2. 產生遷移
docker exec -it hotel_backend alembic revision --autogenerate -m "說明"
# 3. 套用
docker exec -it hotel_backend alembic upgrade head
# 4. 提交
git add backend/models.py backend/alembic/versions/*.py
git commit -m "Database change: 說明"
git push
```

### 同步他人的變更
```powershell
git pull
docker compose restart backend
docker exec -it hotel_backend alembic upgrade head
```

---

**最後更新**：2025-10-29  
**維護者**：vmp010
