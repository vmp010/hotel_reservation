from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    hotel_id = Column(Integer)

class hotel(Base):
    __tablename__ = "hotel_rooms"

    id = Column(Integer, primary_key=True, index=True)
    hotel_Name = Column(String(10), unique=True, index=True)
    location = Column(String(100),nullable=False)
    room_type = Column(String(50))
    price = Column(Integer)
    user_id = Column(Integer)