# 團隊公告：資料庫遷移系統 (Alembic) 已設定完成

嗨團隊成員們！👋

我們已經設定好 **Alembic** 資料庫遷移系統，讓大家更容易管理資料庫變更。

---

## 🎯 這是什麼？

以後當我們需要修改資料庫（例如新增欄位、修改表格），不需要：
- ❌ 手動在 phpMyAdmin 修改
- ❌ 刪除整個資料庫重建
- ❌ 擔心資料遺失

而是：
- ✅ 修改 `models.py`
- ✅ 執行一個指令自動產生遷移
- ✅ 套用到資料庫（保留現有資料）

---

## 🚀 你需要做什麼？（5 分鐘）

### 如果你已經有本地環境：

```powershell
git pull
docker compose down
docker compose up -d --build
docker exec -it hotel_backend alembic upgrade head
```

### 如果你是第一次設定：

```powershell
git clone https://github.com/vmp010/hotel_reservation.git
cd hotel_reservation
docker compose up -d --build
docker exec -it hotel_backend alembic upgrade head
```

### 驗證成功：
開啟 http://localhost:8080（phpMyAdmin）應該看到：
- ✅ `users` 表
- ✅ `hotel_rooms` 表
- ✅ `alembic_version` 表

---

## 📝 以後如何修改資料庫？

### 例如：想在 User 表加 `phone` 欄位

**1. 修改 `backend/models.py`**
```python
class User(Base):
    # ... 其他欄位
    phone = Column(String(20), nullable=True)  # 新增這行
```

**2. 執行指令**
```powershell
docker exec -it hotel_backend alembic revision --autogenerate -m "add phone"
docker exec -it hotel_backend alembic upgrade head
```

**3. 提交**
```powershell
git add backend/models.py backend/alembic/versions/*.py
git commit -m "Database: add phone column to users"
git push
```

**4. 其他人同步**
```powershell
git pull
docker compose restart backend
docker exec -it hotel_backend alembic upgrade head
```

---

## 📚 文件在哪裡？

- **快速開始**：[QUICKSTART.md](QUICKSTART.md) - 常用指令清單
- **完整指南**：[ALEMBIC_SETUP.md](ALEMBIC_SETUP.md) - 詳細說明和最佳實踐
- **變更記錄**：[ALEMBIC_CHANGES.md](ALEMBIC_CHANGES.md) - 我們改了什麼

---

## ❓ 常見問題

**Q: 我不懂資料庫遷移，會不會很難？**  
A: 不會！大部分時候只需要複製貼上上面的指令。Alembic 會自動幫你處理。

**Q: 我正在做的功能會受影響嗎？**  
A: 只要執行 `docker exec -it hotel_backend alembic upgrade head` 同步資料庫就好，你的程式碼不需要改。

**Q: 如果我搞砸了怎麼辦？**  
A: 開發環境可以隨時重置：
```powershell
docker compose down
docker volume rm hotel_reservation_db_data
docker compose up -d --build
docker exec -it hotel_backend alembic upgrade head
```

**Q: 生產環境呢？**  
A: 永遠先備份！然後小心地執行遷移。詳見 [ALEMBIC_SETUP.md](ALEMBIC_SETUP.md)

---

## 🙏 請大家：

1. ✅ 本週內完成本地環境更新
2. ✅ 以後修改資料庫結構都使用 Alembic
3. ✅ 遇到問題先看文件，再問我

---

有任何問題隨時在群組裡問！💬

感謝配合！🎉
