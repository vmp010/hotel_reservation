from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import bcrypt
import auth
from auth import get_current_user

app = FastAPI()
app.include_router(auth.router)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# 註解掉 create_all，改用 Alembic 管理資料庫結構
# models.Base.metadata.create_all(bind=engine)

class HotelRoomCreate(BaseModel):
    hotel_name: str
    location: str
    room_type: str
    price: int | None = None
    # owner: int | None = None



# class UserCreate(BaseModel):
#     username: str
#     email: EmailStr
#     password: str
#     # hotel_id: int | None = None


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    # hotel_id: int | None = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    # hotel_id: int | None = None
    message: str

    class Config:
        from_attributes = True


class HotelOut(BaseModel):
    id: int
    hotel_name: str
    location: str
    room_type: str
    price: int | None = None
    owner: int | None = None

    class Config:
        from_attributes = True

class CartItemCreate(BaseModel):
    hotel_id: int

class OwnerReigister(BaseModel):
    name: str
    email: EmailStr
    password: str

class OwnerLogin(BaseModel):
    email: EmailStr
    password: str

def get_db():
    db = SessionLocal()
    try:
        yield db #測試
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# @app.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
# async def create_user(user: UserCreate, db: db_dependency):
#     # Check for duplicate username or email
#     existing_user = (
#         db.query(models.User)
#         .filter((models.User.username == user.username) | (models.User.email == user.email))
#         .first()
#     )
#     if existing_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already registered")

#     # Hash password using bcrypt
#     hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

#     db_user = models.User(
#         username=user.username,
#         email=user.email,
#         password=hashed_password,
#         # hotel_id=user.hotel_id,
#     )
#     db.add(db_user)
#     db.commit()
#     db.refresh(db_user)
#     return db_user


@app.post("/login/", response_model=LoginResponse)
async def login(user: UserLogin, db: db_dependency):
    # 查找使用者（使用 email）
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email 或密碼錯誤"
        )
    
    # 驗證密碼
    if not bcrypt.checkpw(user.password.encode("utf-8"), db_user.password.encode("utf-8")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Email 或密碼錯誤"
        )
    
    # 登入成功，回傳使用者資訊
    return LoginResponse(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        # hotel_id=db_user.hotel_id,
        message="登入成功"
    )

@app.post("/create_hotel/", response_model=HotelRoomCreate, status_code=status.HTTP_201_CREATED)
async def create_room(hotel: HotelRoomCreate, db: db_dependency):
    db_room = models.Hotel(
        hotel_name=hotel.hotel_name,
        location=hotel.location,
        room_type=hotel.room_type,
        price=hotel.price,
        owner=hotel.owner
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room

@app.get("/hotels/")
def read_hotels(db: db_dependency):
    hotels = db.query(models.Hotel).all()
    return hotels

@app.get("/hotels/{hotel_id}")
def read_hotel(hotel_id: int, db: db_dependency):
    hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel

@app.get("/index/")
def read_index( db: db_dependency, limit: int = 3):
    hotels = db.query(models.Hotel).all()[:limit]
    if not hotels:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotels



@app.get("/delHotel/{hotel_id}")
def delete_hotel(hotel_id: int, db: db_dependency):
    hotel = db.query(models.Hotel).filter(models.Hotel.id == hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=404, detail="Hotel not found")
    db.delete(hotel)
    db.commit()
    return {"detail": "Hotel deleted successfully"}


@app.post("/users/{user_id}/cart", response_model=HotelOut, status_code=status.HTTP_201_CREATED)
async def add_to_cart(user_id: int, item: CartItemCreate, db: db_dependency):
    # 檢查使用者是否存在
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    # 檢查飯店是否存在
    db_hotel = db.query(models.Hotel).filter(models.Hotel.id == item.hotel_id).first()
    if not db_hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    
    # 檢查是否已在購物車
    if db_hotel in db_user.carts:
        raise HTTPException(status_code=400, detail="Hotel already in cart")
    
    # ✅ 正確：使用 relationship 加入
    db_user.carts.append(db_hotel)
    db.commit()
    db.refresh(db_hotel)
    
    return db_hotel

@app.get("/users/{user_id}/cart", response_model=list[HotelOut])
async def get_cart(user_id: int, db: db_dependency):
    """取得使用者購物車內容"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user.carts

@app.delete("/users/{user_id}/cart")
async def clear_cart(user_id: int, db: db_dependency):
    """清空購物車"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.carts.clear()
    db.commit()
    return {"detail": "Cart cleared"}

@app.get("/",status_code=200)
async def user(user: user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail="Invalid authentication credentials")
    return {"User":user}

@app.post("/owners/register", status_code=status.HTTP_201_CREATED)
async def register_owner(owner: OwnerReigister, db: db_dependency):
    # Check for duplicate email
    existing_owner = db.query(models.Owner).filter(models.Owner.email == owner.email).first()
    if existing_owner:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    # Hash password using bcrypt
    hashed_password = bcrypt.hashpw(owner.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    db_owner = models.Owner(
        name=owner.name,
        email=owner.email,
        password=hashed_password
    )
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

@app.post("/owners/login", response_model=LoginResponse)
async def login_owner(owner: OwnerLogin, db: db_dependency):
    db_owner = db.query(models.Owner).filter(models.Owner.email == owner.email).first()
    if not db_owner:
        raise HTTPException(status_code=401, detail="Email 或密碼錯誤")
    
    # 驗證密碼
    if not bcrypt.checkpw(owner.password.encode("utf-8"), db_owner.password.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Email 或密碼錯誤")


# #管理每次 API 請求的資料庫連線
# def get_session(): 
#     with Session(engine) as session:
#         yield session

# @app.post("/rooms/") #新增，提交
# def create_Room(room:Room,session:Session=Depends(get_session)):
#     session.add(room)
#     session.commit() #提交
#     session.refresh(room)
#     return room #回傳json檔

# @app.get("/rooms/") #查詢
# def read_rooms(session:Session=Depends(get_session)):
#     rooms=session.query(Room).all()
#     return rooms