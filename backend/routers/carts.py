from models import User,Hotel
from fastapi import APIRouter, Depends, HTTPException, status
from auth import get_current_user, db_dependency
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/carts",
    tags=["carts"]
)

@router.post("/{hotel_id}", status_code=status.HTTP_201_CREATED)
async def add_hotel_to_cart(hotel_id: int, 
                            db: db_dependency,
                            user: dict = Depends(get_current_user)):
    
    db_user = db.query(User).filter(User.id == user["id"]).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    hotel=db.query(Hotel).filter(Hotel.id==hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    
    if hotel in db_user.carts:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Hotel already in cart")
    
    db_user.carts.append(hotel)
    db.commit()
    
    return{"message":f'Hotel {hotel.hotel_name} added to cart successfully'}

@router.get("/", status_code=status.HTTP_200_OK)
async def get_user_cart(db: db_dependency,
                        user: dict = Depends(get_current_user)):
    
    db_user = db.query(User).filter(User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return db_user.carts

@router.delete("/{hotel_id}", status_code=status.HTTP_200_OK)
async def remove_hotel_from_cart(db: db_dependency,
                                hotel_id: int, 
                                 user: dict = Depends(get_current_user)):
    
    db_user = db.query(User).filter(User.id == user["id"]).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    hotel=db.query(Hotel).filter(Hotel.id==hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    
    if hotel not in db_user.carts:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Hotel not in cart")
    
    db_user.carts.remove(hotel)
    db.commit()
    
    return None






