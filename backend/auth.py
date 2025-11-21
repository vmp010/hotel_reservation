from datetime import datetime, timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, APIRouter, status
from pydantic import BaseModel, EmailStr
from database import SessionLocal
from sqlalchemy.orm import Session
from models import User,Owner
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
OAuth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

class CreateUserRequest(BaseModel):
    username: str
    email: EmailStr
    password: str

class CreateOwnerRequest(BaseModel):
    owner_name: str
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    role: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/register/user", status_code=201)
def register_user(user: CreateUserRequest, db: db_dependency):
    hashed_password = bcrypt_context.hash(user.password)
    if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")
    
    create_user_model = User(username=user.username, email=user.email, password=hashed_password)

    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    

def authenticate_user(db, username: str, password: str):
    user=db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.password):
        return False
    return user

async def get_current_user(token: Annotated[str, Depends(OAuth2_bearer)], db: db_dependency):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")
        if username is None or user_id is None or role != "user":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="權限不足",
            )
        user=db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="使用者不存在",
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

##店家
@router.post("/register/owner",status_code=status.HTTP_201_CREATED)
def register_owner(owner: CreateOwnerRequest, db: db_dependency):
    hashed_password = bcrypt_context.hash(owner.password)
    create_owner_model = Owner(owner_name=owner.owner_name, email=owner.email, password=hashed_password)

    db.add(create_owner_model)
    db.commit()
    db.refresh(create_owner_model)

#店家登入
# @router.post("/token/owner", response_model=Token)
# async def owner_login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency ):
#     owner=authenticate_owner(db,form_data.username,form_data.password)
#     if not owner:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Incorrect username or password",
#         )
#     token=create_access_token(owner.username,owner.id,"owner",timedelta(minutes=30))
#     return {"access_token":token,"token_type":"bearer"}



def authenticate_owner(db, username: str, password: str):
    owner=db.query(Owner).filter(Owner.owner_name == username).first()
    if not owner:
        return False
    if not bcrypt_context.verify(password, owner.password):
        return False
    return owner

#統一登入
@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency ):
  input_email=form_data.username
  input_password=form_data.password

  owner=db.query(Owner).filter(Owner.email == input_email).first()
  if owner and bcrypt_context.verify(input_password, owner.password):
      token=create_access_token(owner.owner_name,owner.id,"owner",timedelta(minutes=30))
      return {"access_token":token,"token_type":"bearer","role":"owner"}
  
  user=db.query(User).filter(User.email == input_email).first()
  if user and bcrypt_context.verify(input_password, user.password):
      token=create_access_token(user.username,user.id,"user",timedelta(minutes=30))
      return {"access_token":token,"token_type":"bearer","role":"user"}
  raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Incorrect username or password",
  )

def create_access_token(username: str, user_id: int,role:str, expires_delta: timedelta):
    encode={"sub":username,"id":user_id,"role":role}
    expires=datetime.utcnow()+expires_delta
    encode.update({"exp":expires})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)


    
async def get_current_owner(token: Annotated[str, Depends(OAuth2_bearer)], db: db_dependency):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        owner_name: str = payload.get("sub")
        owner_id: int = payload.get("id")
        role: str = payload.get("role")
        if owner_name is None or owner_id is None or role != "owner":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
        owner=db.query(Owner).filter(Owner.id == owner_id).first()
        if owner is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Owner does not exist",
            )
        return owner
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )