from sqlalchemy import Column, ForeignKey, Integer, String,Table
from sqlalchemy.orm import relationship
from database import Base

user_cart = Table(
    'user_hotel',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id',ondelete="CASCADE"),primary_key=True),
    Column('hotel_id', Integer, ForeignKey('hotel_rooms.id',ondelete="CASCADE"),primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100))
    # hotel_id = Column(Integer, ForeignKey("hotel_rooms.id"))

    carts=relationship(
        "Hotel",
        secondary=user_cart,
        back_populates="users",
        passive_deletes=True
    )

class Hotel(Base):
    __tablename__ = "hotel_rooms"

    id = Column(Integer, primary_key=True, index=True)
    hotel_name = Column(String(100), index=True)
    location = Column(String(100),nullable=False)
    room_type = Column(String(50))
    price = Column(Integer)
    owner_id=Column(Integer,ForeignKey("owners.id",ondelete="CASCADE"),nullable=False)

    owner_rel=relationship("Owner",back_populates="hotels")
    users=relationship("User",secondary=user_cart,back_populates="carts",passive_deletes=True)
    # user_id = Column(Integer,ForeignKey("users.id"))

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    owner_name = Column(String(100), unique=True, index=True)
    email = Column(String(100), unique=True, index=True)
    password = Column(String(100),nullable=False)

    hotels= relationship("Hotel", back_populates="owner_rel", passive_deletes=True)