from datetime import datetime, date
from models import User,Hotel,Booking
from fastapi import APIRouter, Depends, HTTPException, status
from auth import get_current_user, db_dependency
from sqlalchemy.orm import Session
from schemas import CartItemResponse

router = APIRouter(
    prefix="/carts",
    tags=["carts"]
)

@router.post("/add/{hotel_id}", status_code=status.HTTP_201_CREATED)
async def add_hotel_to_cart(hotel_id: int, 
                            db: db_dependency,
                            user: User = Depends(get_current_user)):
    
    db_user = db.query(User).filter(User.id == user.id).first()
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
                        user: User = Depends(get_current_user)):
    today_str=date.today().strftime("%Y-%m-%d")
    user_bookings=db.query(Booking).filter(
        Booking.user_id==user.id,
        Booking.checkin_date>=today_str
    ).all()
    
    cart_items=[]
    for booking in user_bookings:
        hotel=booking.hotel_rel

        if not hotel:
            continue
        c_in_obj=date.today()
        c_out_obj=date.today()
        nights=1

        try:
            c_in_obj = datetime.strptime(booking.checkin_date, "%Y-%m-%d").date()
            c_out_obj = datetime.strptime(booking.checkout_date, "%Y-%m-%d").date()

            delta = c_out_obj - c_in_obj
            nights =delta.days
        except:
            print("日期轉換錯誤")
            nights=1

       

        if nights < 1:
            nights = 1

        total_price=hotel.price * nights

        cart_items.append(CartItemResponse(
            booking_id=booking.id,
            hotel_name=hotel.hotel_name,
            location=hotel.location,
            room_type=hotel.room_type,
            price_per_night=hotel.price,
            check_in=c_in_obj,
            check_out=c_out_obj,
            total_days=nights,
            total_price=total_price
        ))

    return cart_items

@router.delete("/delete/{hotel_id}", status_code=status.HTTP_200_OK)
async def remove_hotel_from_cart(db: db_dependency,
                                hotel_id: int, 
                                 user: User = Depends(get_current_user)):
    
    db_user = db.query(User).filter(User.id == user.id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    hotel=db.query(Hotel).filter(Hotel.id==hotel_id).first()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Hotel not found")
    
    if hotel  in db_user.carts:
        db_user.carts.remove(hotel)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Hotel not in cart")

    booking_to_delete=db.query(Booking).filter(
        Booking.user_id==db_user.id,
        Booking.hotel_id==hotel.id,
        Booking.checkin_date>=datetime.date.today() #不將過去紀錄也刪除
    ).all()

    for booking in booking_to_delete:
        db.delete(booking)

    
    
    db.commit()
    
    return None






