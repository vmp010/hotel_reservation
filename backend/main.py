from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import bcrypt

app = FastAPI()

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

class HotelRoomBase(BaseModel):
    room_number: str
    room_type: str
    price: int
    user_id: int

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    hotel_id: int | None = None


class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    hotel_id: int | None = None

    class Config:
        from_attributes = True

def get_db():
    db = SessionLocal()
    try:
        yield db #測試
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: db_dependency):
    # Check for duplicate username or email
    existing_user = (
        db.query(models.User)
        .filter((models.User.username == user.username) | (models.User.email == user.email))
        .first()
    )
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already registered")

    # Hash password using bcrypt
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    db_user = models.User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        hotel_id=user.hotel_id,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
   




@app.get("/")
def read_root():
    return {"Hello": "World"} 

#驗光好菜          

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