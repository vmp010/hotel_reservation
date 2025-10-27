from fastapi import FastAPI, HTTPException, Depends,status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session


app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class HotelRoomBase(BaseModel):
    room_number: str
    room_type: str
    price: int
    user_id: int

class UserBase(BaseModel):
    username: str
    email: str
    password: str
    hotel_id: int

def get_db():
    db = SessionLocal()
    try:
        yield db #測試
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(
      **user.dict()
    )
    db.add(db_user)
    db.commit()
   




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