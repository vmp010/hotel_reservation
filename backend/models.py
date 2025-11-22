from sqlalchemy import Column, ForeignKey, Integer, String,Table,Boolean,Text,DateTime
from sqlalchemy.sql import func
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

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id",ondelete="CASCADE"), nullable=False)
    hotel_id = Column(Integer, ForeignKey("hotel_rooms.id",ondelete="CASCADE"), nullable=False)
    checkin_date = Column(String(20), nullable=False) #入住日
    checkout_date = Column(String(20), nullable=False)  #退房日

    is_active = Column(Boolean, default=1)  # 1表示有效，0表示取消
    
    user_rel = relationship("User", passive_deletes=True)
    hotel_rel = relationship("Hotel", passive_deletes=True)

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    
    # 關聯欄位
    user_id = Column(Integer, ForeignKey("users.id"))
    hotel_id = Column(Integer, ForeignKey("hotel_rooms.id")) # 對應你的 Hotel model
    booking_id = Column(Integer, ForeignKey("bookings.id"))  # 🔥 關鍵：綁定訂單，確保是真實入住
    
    # 內容欄位
    rating = Column(Integer, nullable=False) # 1~5 分
    comment = Column(Text, nullable=True)    # 文字內容
    
    # 商家回覆 (Optional)
    reply = Column(Text, nullable=True)      # 店家可以回覆
    
    # 時間欄位 (自動生成)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 建立關聯，方便查詢
    user = relationship("User", backref="reviews")
    hotel = relationship("Hotel", backref="reviews")
    booking = relationship("Booking")