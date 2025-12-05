from datetime import datetime, timedelta
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, APIRouter, status,Response,Request
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
ACCESS_TOKEN_EXPIRE_MINUTES =30
REFRESH_TOKEN_EXPIRE_DAYS =7

bcrypt_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token",auto_error=False)

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

def create_token(data: dict, expires_delta: timedelta=None ):
    to_encode = data.copy()
    if expires_delta:
        expire=datetime.utcnow()+expires_delta
    else:
        expire=datetime.utcnow()+timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_access_token(username: str, user_id: int, role: str, email: str, expires_delta: timedelta=None):
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    return create_token(
        data={"sub": username, "id": user_id, "role": role, "email": email},
        expires_delta=expires_delta
    )

def create_refresh_token(username: str, user_id: int, role: str, email: str, expires_delta: timedelta=None):
    if expires_delta is None:
        expires_delta = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    return create_token(
        data={"sub": username, "id": user_id, "role": role, "email": email},
        expires_delta=expires_delta
    )

@router.post("/register/user", status_code=201)
def register_user(user: CreateUserRequest, db: db_dependency):
    hashed_password = bcrypt_context.hash(user.password)
    if db.query(User).filter((User.username == user.username) | (User.email == user.email)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username or email already exists")
    
    if db.query(Owner).filter(Owner.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered as owner")
    
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


##店家
@router.post("/register/owner",status_code=status.HTTP_201_CREATED)
def register_owner(owner: CreateOwnerRequest, db: db_dependency):
    if db.query(Owner).filter((Owner.owner_name == owner.owner_name) | (Owner.email == owner.email)).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Owner name or email already exists")
    
    if db.query(User).filter(User.email == owner.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered as user")
    
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
@router.post("/token")
async def login_for_access_token(
    response: Response, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    db: db_dependency 
):
    input_email = form_data.username
    input_password = form_data.password
    
    user_obj = None
    role = None

    # A. 檢查 Owner
    owner = db.query(Owner).filter(Owner.email == input_email).first()
    if owner and bcrypt_context.verify(input_password, owner.password):
        user_obj = owner
        role = "owner"
        username = owner.owner_name
    
    # B. 檢查 User
    if not user_obj:
        user = db.query(User).filter(User.email == input_email).first()
        if user and bcrypt_context.verify(input_password, user.password):
            user_obj = user
            role = "user"
            username = user.username

    # C. 驗證失敗
    if not user_obj:
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # D. 產生 Tokens
    access_token = create_access_token(username, user_obj.id, role, user_obj.email,timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    refresh_token = create_refresh_token(username, user_obj.id, role)

    # E. 設定 Cookies
    # 1. Access Token (短效)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        samesite="lax",
        secure=False  # 上線改 True
    )

    # 2. Refresh Token (長效，限制路徑)
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        samesite="lax",
        secure=False, # 上線改 True
        path="/auth/refresh" # 🔥 安全關鍵：只有換票 API 能讀到這個 Cookie
    )

    return {"message": "Login successful", "role": role}
# def create_access_token(username: str, user_id: int,role:str, email:str, expires_delta: timedelta):
#     encode={"sub":username,"id":user_id,"role":role,"email":email}
#     expires=datetime.utcnow()+expires_delta
#     encode.update({"exp":expires})
#     return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

@router.post("/refresh")
async def refresh_access_token(request:Request, response: Response, db: db_dependency):
    refresh_token=request.cookies.get("refresh_token")

    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token missing")
    try:
        payload=jwt.decode(refresh_token,SECRET_KEY,algorithms=[ALGORITHM])

        if payload.get("type")!="refresh":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token type")
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")

        if role=="user":
            user=db.query(User).filter(User.id == user_id).first()
            email=user.email if user else ""
        elif role=="owner":
            owner=db.query(Owner).filter(Owner.id == user_id).first()
            user=owner
            email=owner.email if owner else ""
        
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
        
        new_access_token=create_access_token(username,user_id,role,email)

        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            samesite="lax",
            secure=False  # 上線改 True
        )
        return {"message":"Access token refreshed"}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    

@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token", path="/auth/refresh")
    return {"message":"Logged out successfully"}

async def get_current_user(
        request: Request,
         db: db_dependency,
        token: Optional[str] = Depends(OAuth2_scheme),
):
    cookie_token=request.cookies.get("access_token")
    final_token=cookie_token if cookie_token else token

    if not final_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    try:
        payload=jwt.decode(final_token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        role: str = payload.get("role")

        if role != "user":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="權限不足",
            )
        user=db.query(User).filter(User.id == user_id).first()
        if username is None :
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="使用者不存在"
            )
        return user
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token無效",
        )

async def get_current_owner(
    request: Request, 
    db: db_dependency,
    token: Optional[str] = Depends(OAuth2_scheme) 
):
    cookie_token=request.cookies.get("access_token")
    final_token=cookie_token if cookie_token else token

    if not final_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
    try:
        payload=jwt.decode(final_token,SECRET_KEY,algorithms=[ALGORITHM])
        
        owner_id: int = payload.get("id")
        role: str = payload.get("role")
        if role != "owner":
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
            detail="token無效"
        )
@router.get("/me")
async def read_me(request: Request, db: db_dependency):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401)
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        role = payload.get("role")
        user_id = payload.get("id")
        
        if role == "user":
            user = db.query(User).filter(User.id == user_id).first()
            return {"id": user.id, "username": user.username, "role": "user", "email": user.email}
            
        elif role == "owner":
            owner = db.query(Owner).filter(Owner.id == user_id).first()
            return {"id": owner.id, "owner_name": owner.owner_name, "role": "owner", "email": owner.email}
            
    except JWTError:
        raise HTTPException(status_code=401)
