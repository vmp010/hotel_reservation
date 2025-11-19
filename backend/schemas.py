from typing import List
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