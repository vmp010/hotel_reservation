from typing import List,Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import date,datetime

class HotleDisplay(BaseModel):
    id: int
    hotel_name: str
    location: str
    room_type: str
    price: int | None = None
    owner_id: int | None = None

    class Config:
        orm_mode = True
        from_attributes = True

class HotelCreate(BaseModel):
    hotel_name: str
    location: str
    room_type: str
    price: int

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    hotel_id: int
    checkin_date: str
    checkout_date: str

class BookingResponse(BaseModel):
    id: int
    user_id: int
    # hotel_id: int
    # checkin_date: str
    # checkout_date: str
    # is_active: bool

    class Config:
        from_attributes = True

class CartItemResponse(BaseModel):
    booking_id: int
    hotel_name: str
    location: str
    room_type: str
    price_per_night: int  # 單晚價格
    check_in: date
    check_out: date
    total_days: int       # 住幾晚
    total_price: int      # 總金額

    class Config:
        from_attributes = True

class CartAddRequest(BaseModel):
    checkin_date: date
    checkout_date: date

# 編輯時用的模型
class HotelEditRequest(BaseModel):
    hotel_name: Optional[str] = None
    location: Optional[str] = None
    room_type: Optional[str] = None
    price: Optional[int] = None
    

    class Config:
        from_attributes = True


class OwnerBookingResponse(BaseModel):
    booking_id: int
    hotel_name: str
    room_type: str
    guest_name: str    # 訂房人姓名
    guest_email: str   # 訂房人 Email (方便聯絡)
    check_in: str      # 入住日
    check_out: str     # 退房日
    is_active: bool    # 訂單狀態

    class Config:
        from_attributes = True

class UserBookingResponse(BaseModel):
    booking_id: int
    hotel_name: str
    location: str
    room_type: str
    price_per_night: int
    check_in: date      # 前端拿到的會是標準日期格式
    check_out: date
    total_price: int    # 我們會在後端算好總價傳過去
    is_active: bool     # 顯示是「已預訂」還是「已取消」

    class Config:
        from_attributes = True


# 使用者新增評論時的輸入
class ReviewCreate(BaseModel):
    hotel_id: int
    booking_id: int
    rating: int = Field(..., ge=1, le=5) # 限制 1~5 分
    comment: str

# 回傳給前端顯示用
class ReviewResponse(BaseModel):
    id: int
    user_id: int
    username: str # 為了前端顯示名字，我們之後手動填入
    rating: int
    comment: str
    reply: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


