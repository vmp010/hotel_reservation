# 資料庫遷移指南 (Alembic)

## 📋 概念說明

**Alembic** 是 SQLAlchemy 的資料庫遷移工具，可以：
- ✅ 自動偵測 model 變更
- ✅ 產生遷移腳本
- ✅ 保留現有資料
- ✅ 可回溯到之前的版本

---

## 🚀 使用流程

### 1️⃣ 修改 Model
在 `models.py` 中修改你的資料表結構，例如：
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    hotel_id = Column(Integer)
    # 新增欄位
    phone = Column(String(20), nullable=True)
```

### 2️⃣ 進入後端容器
```powershell
docker exec -it hotel_backend bash
```

### 3️⃣ 產生遷移檔
```bash
# 自動偵測變更並產生遷移腳本
alembic revision --autogenerate -m "add phone column to users"
```

**說明**：
- `--autogenerate`: 自動比對 model 和資料庫，產生差異
- `-m "訊息"`: 描述這次變更的內容

### 4️⃣ 套用遷移
```bash
# 將變更套用到資料庫
alembic upgrade head
```

**結果**：資料庫表格結構已更新，原有資料保留！

---

## 🔄 常用指令

### 查看目前版本
```bash
alembic current
```

### 查看遷移歷史
```bash
alembic history
```

### 回溯到上一個版本
```bash
alembic downgrade -1
```

### 回溯到特定版本
```bash
alembic downgrade <revision_id>
```

### 升級到最新版本
```bash
alembic upgrade head
```

---

## 📝 完整範例

### 情境：新增 `phone` 欄位到 User 表格

**步驟 1**：修改 `models.py`
```python
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    hotel_id = Column(Integer)
    phone = Column(String(20), nullable=True)  # 新增這行
```

**步驟 2**：產生遷移
```powershell
# 在本機 PowerShell
docker exec -it hotel_backend alembic revision --autogenerate -m "add phone to users"
```

**步驟 3**：套用變更
```powershell
docker exec -it hotel_backend alembic upgrade head
```

**完成**！去 phpMyAdmin 檢查，`users` 表格已經有 `phone` 欄位了。

---

## ⚠️ 注意事項

1. **第一次使用**：需要建立初始遷移
   ```bash
   # 為現有資料庫建立基準
   alembic revision --autogenerate -m "initial migration"
   alembic upgrade head
   ```

2. **刪除欄位**：Alembic 會產生 DROP COLUMN，請確認不會遺失重要資料

3. **修改欄位類型**：可能需要手動調整遷移腳本

4. **開發環境快速重置**：如果只是開發測試，可以直接刪除 volume 重建
   ```powershell
   docker compose down
   docker volume rm hotel_reservation_db_data
   docker compose up -d
   ```

---

## 🎯 生產環境最佳實踐

1. **總是先在開發環境測試遷移**
2. **備份資料庫再執行遷移**
3. **檢查產生的遷移腳本是否正確**
4. **記錄每次遷移的目的和時間**

---

## 🔧 故障排除

### 問題：Alembic 沒有偵測到變更
**解決**：
1. 確認 `alembic/env.py` 有正確導入 `Base.metadata`
2. 確認 model 類別有繼承 `Base`
3. 確認 `__tablename__` 正確

### 問題：資料庫連線失敗
**解決**：
```bash
# 檢查環境變數
echo $DATABASE_URL

# 手動指定
alembic -x dbUrl=mysql+pymysql://admin:admin123@db:3306/hotel_reservation upgrade head
```

### 問題：遷移衝突
**解決**：
```bash
# 查看當前狀態
alembic current

# 強制同步到最新
alembic stamp head
```
