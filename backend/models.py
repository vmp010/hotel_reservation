from sqlalchemy import Column, ForeignKey, Integer, String,Table
from sqlalchemy.orm import relationship
from database import Base

user_hotel_association = Table(
    'user_hotel_association',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'),primary_key=True),
    Column('hotel_id', Integer, ForeignKey('hotel_rooms.id'),primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    # hotel_id = Column(Integer, ForeignKey("hotel_rooms.id"))

    hotels=relationship(
        "Hotel",
        secondary=user_hotel_association,
        back_populates="users"
    )

class Hotel(Base):
    __tablename__ = "hotel_rooms"

    id = Column(Integer, primary_key=True, index=True)
    hotel_name = Column(String(100), unique=True, index=True)
    location = Column(String(100),nullable=False)
    room_type = Column(String(50))
    price = Column(Integer)
    # user_id = Column(Integer,ForeignKey("users.id"))

    users=relationship(
        "User",
        secondary=user_hotel_association,
        back_populates="hotels"
    )