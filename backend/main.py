from fastapi import FastAPI, HTTPException, Depends, status
from typing import Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.sql import func
import auth
from auth import get_current_user,get_current_owner
from routers import carts, hotels, booking,reviews

app = FastAPI()
app.include_router(auth.router)
app.include_router(carts.router)

app.include_router(hotels.router)
app.include_router(booking.router)

app.include_router(reviews.router)

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
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db #測試
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]
owner_dependency = Annotated[dict, Depends(get_current_owner)]



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
    hotels = db.query(models.Hotel)\
                .group_by(models.Hotel.hotel_name)\
                .order_by(func.random())\
                .limit(limit).all()
    
    if not hotels:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotels



@app.get("/get_current_user",status_code=status.HTTP_200_OK)
async def user(user: user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication credentials")
    return {"User":user}

@app.get("/get_current_owner",status_code=status.HTTP_200_OK)
async def owner(owner: owner_dependency,db: db_dependency):
    if owner is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication credentials")
    return {"Owner":owner}

