from sqlalchemy import Column, ForeignKey, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    hotel_id = Column(Integer, ForeignKey("hotel_rooms.id"))

class Hotel(Base):
    __tablename__ = "hotel_rooms"

    id = Column(Integer, primary_key=True, index=True)
    hotel_name = Column(String(10), unique=True, index=True)
    location = Column(String(100),nullable=False)
    room_type = Column(String(50))
    price = Column(Integer)
    user_id = Column(Integer,ForeignKey("users.id"))