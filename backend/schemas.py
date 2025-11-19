from typing import List,Optional
from pydantic import BaseModel

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