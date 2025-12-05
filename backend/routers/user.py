from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import User,Owner
from auth import get_current_user,db_dependency,bcrypt_context
from schemas import UpdateUserEmailRequest,UpdateUserPasswordRequest

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.put("/update_email", status_code=status.HTTP_200_OK)
async def update_user_email(
    email_request: UpdateUserEmailRequest,
    db: db_dependency,
    user: User = Depends(get_current_user)
):
    if db.query(User).filter(User.email == email_request.new_email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    
    if db.query(Owner).filter(Owner.email == email_request.new_email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    
    user.email = email_request.new_email
    db.commit()
    return {"message": "Email updated successfully"}

@router.put("/update_password", status_code=status.HTTP_200_OK)
async def update_user_password(
    request: UpdateUserPasswordRequest,
    db: db_dependency,
    user: User = Depends(get_current_user)
):
    if not bcrypt_context.verify(request.old_password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Current password is incorrect")
    
    user.password = bcrypt_context.hash(request.new_password)
    db.commit()
    return {"message": "Password updated successfully"}