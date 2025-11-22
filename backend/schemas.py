from typing import List,Optional
from pydantic import BaseModel
from datetime import datetime

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

from pydantic import BaseModel
from typing import Optional

# 編輯時用的模型
class HotelEditRequest(BaseModel):
    hotel_name: Optional[str] = None
    location: Optional[str] = None
    room_type: Optional[str] = None
    price: Optional[int] = None
    

    class Config:
        from_attributes = True