from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models import Hotel, Owner
from auth import get_current_owner,db_dependency
from schemas import HotelCreate

router = APIRouter(
    prefix="/hotels",
    tags=["hotels"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_hotel(hotel: HotelCreate,
                       db: db_dependency,
                       current_owner: Owner = Depends(get_current_owner)):
    
    db_owner = db.query(Owner).filter(Owner.id == current_owner.id).first()
    if not db_owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found")
    
    new_hotel = Hotel(
        hotel_name=hotel.hotel_name,
        location=hotel.location,
        room_type=hotel.room_type,
        price=hotel.price,
        owner_id=current_owner.id
    )
    
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    
    return {"message": f'Hotel {new_hotel.hotel_name} created successfully', "hotel_id": new_hotel.id}

@router.delete("/delete/{hotel_id}", status_code=status.HTTP_200_OK)
async def delete_hotel(hotel_id: int,
                       db: db_dependency,
                       current_owner: Owner = Depends(get_current_owner)):
    
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id, Hotel.owner_id == current_owner.id).first()
    
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found or not owned by you")
    
    db.delete(hotel)
    db.commit()
    
    return {"message": f'Hotel {hotel.hotel_name} deleted successfully'}

@router.get("/my_hotels", status_code=status.HTTP_200_OK)
async def get_my_hotels(db: db_dependency,
                        current_owner: Owner = Depends(get_current_owner)):
    
    hotels = db.query(Hotel).filter(Hotel.owner_id == current_owner.id).all()
    
    return {"hotels": hotels}