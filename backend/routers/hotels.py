from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import func
from models import Hotel, Owner
from auth import get_current_owner
from auth import db_dependency
from schemas import HotelCreate, HotelEditRequest

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

@router.get("/owner/index/",status_code=status.HTTP_200_OK)
async def get_index_hotels(db: db_dependency,
                            current_owner: Owner = Depends(get_current_owner),
                            limit: int = 3):
    
    hotels = db.query(Hotel)\
                .group_by(Hotel.hotel_name)\
                .filter(Hotel.owner_id == current_owner.id)\
                .order_by(Hotel.id.desc())\
                .limit(limit).all()
    
    if not hotels:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No hotels found")
    
    return hotels

@router.get("/my_hotels", status_code=status.HTTP_200_OK)
async def get_my_hotels(db: db_dependency,
                        current_owner: Owner = Depends(get_current_owner)):
    
    hotels = db.query(Hotel).filter(Hotel.owner_id == current_owner.id).all()
    
    return {"hotels": hotels}

@router.patch("/edit/{hotel_id}", status_code=status.HTTP_200_OK)
async def edit_hotel(hotel_id: int,
                     hotel_request: HotelEditRequest,
                     db: db_dependency,
                     current_owner: Owner = Depends(get_current_owner)):
    
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id, Hotel.owner_id == current_owner.id).first()
    
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found or not owned by you")
    
    if hotel.owner_id != current_owner.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to edit this hotel")
    
    update_data = hotel_request.dict(exclude_unset=True) #沒加 exclude_unset=True 的話,會把 None 也更新掉

    for key, value in update_data.items():
        # 告訴 Python：請幫我把 hotel_model 裡面，名稱叫做 key (變數內容) 的那個欄位，改成 value
        setattr(hotel, key, value)

    db.add(hotel)
    db.commit()
    db.refresh(hotel)
   
    
    return hotel