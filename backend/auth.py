from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, status
from pydantic import BaseModel, EmailStr
from database import SessionLocal
from sqlalchemy.orm import Session
from models import User
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.hash import bcrypt

router=APIRouter(
    prefix="/auth",
      tags=["auth"])

SECRET_KEY ="b8a54b0685e4d1f044931b6c6eb34e58"
ALGORITHM ="HS256"

bcrypt_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")
OAuth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/login")

class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register", status_code=201)
def register_user(user: CreateUserRequest, db: db_dependency):
    hashed_password = bcrypt_context.hash(user.password)
    create_user_model = User(username=user.username, email=user.email, password=hashed_password)

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency ):
    user=authenticate_user(db,form_data.username,form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    token=create_access_token(user.username,user.id,timedelta(minutes=30))

    return {"access_token":token,"token_type":"bearer"}

def authenticate_user(db, username: str, password: str):
    user=db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode={"sub":username,"id":user_id}
    expires=datetime.utcnow()+expires_delta
    encode.update({"exp":expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)