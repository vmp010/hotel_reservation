from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from auth import db_dependency
from models import Booking, Hotel, User,Owner
from schemas import BookingCreate, BookingResponse,OwnerBookingResponse,UserBookingResponse
from auth import get_current_user,get_current_owner
from datetime import date,datetime

router = APIRouter(
    prefix="/bookings",
    tags=["bookings"]
)

#查詢日曆用:查詢某間
@router.get("/unavailable_dates/{hotel_id}", status_code=status.HTTP_200_OK)
def get_unavailable_dates(hotel_id: int,
                          db: db_dependency):
    
    existing_Booking = db.query(Booking).filter(
        Booking.hotel_id == hotel_id,
        Booking.is_active == True,
        Booking.checkout_date >= date.today()
        ).all()
    
    return existing_Booking

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=BookingResponse)
def create_booking(booking_request: BookingCreate,
                   db: db_dependency,
                   current_user: User = Depends(get_current_user)):
    if booking_request.checkin_date >= booking_request.checkout_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Check-out date must be after check-in date")
    
    overlap_booking = db.query(Booking).filter(
        Booking.hotel_id == booking_request.hotel_id,
        Booking.is_active == True,
        and_(
            Booking.checkin_date < booking_request.checkout_date,
            Booking.checkout_date > booking_request.checkin_date
        )
    ).first()

    if overlap_booking:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The hotel is already booked for the selected dates")
    
    new_booking = Booking(
        user_id=current_user.id,
        hotel_id=booking_request.hotel_id,
        checkin_date=booking_request.checkin_date,
        checkout_date=booking_request.checkout_date,
        is_active=True
    )

    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@router.get("/myRes",response_model=list[UserBookingResponse],status_code=status.HTTP_200_OK)
async def get_my_booking(
    db:db_dependency,
    user:User=Depends(get_current_user)
):
    today_str=date.today().strftime("%Y-%m-%d")
    my_booking=db.query(Booking).filter(
        Booking.user_id==user.id,
        Booking.status=="PAID",
        Booking.checkin_date>=today_str
    ).all

    results=[]

    for booking in my_booking:
        hotel=booking.hotel_rel

        if not hotel:
            continue

        c_in_obj = date.today()
        c_out_obj = date.today()
        nights = 1

        try:
            c_in_obj = datetime.strptime(booking.checkin_date, "%Y-%m-%d").date()
            c_out_obj = datetime.strptime(booking.checkout_date, "%Y-%m-%d").date()
            
            delta = c_out_obj - c_in_obj
            nights = delta.days
        except:
            print(f"日期轉換錯誤 ID: {booking.id}")
            nights = 1

        if nights < 1:
            nights = 1
            
        total_price = hotel.price * nights

        # 3. 組裝回傳資料
        results.append(UserBookingResponse(
            booking_id=booking.id,
            hotel_name=hotel.hotel_name,
            location=hotel.location,
            room_type=hotel.room_type,
            price_per_night=hotel.price,
            check_in=c_in_obj,
            check_out=c_out_obj,
            total_price=total_price, # 算好的總價
            is_active=booking.is_active
        ))
        
    return results

@router.get("/owner/all", status_code=status.HTTP_200_OK, response_model=list[OwnerBookingResponse])
async def get_owner_bookings(db: db_dependency,
                             current_owner:Owner=Depends(get_current_owner)):
    results=db.query(Booking).join(Hotel).join(User).filter(
        Hotel.owner_id==current_owner.id
    ).all()

    response_list=[]
    for booking in results:
        
        hotel=booking.hotel_rel
        guest=booking.user_rel

        if not hotel or not guest:
            continue

        response_list.append(OwnerBookingResponse(
            booking_id=booking.id,
            hotel_name=hotel.hotel_name,
            room_type=hotel.room_type,
            guest_name=guest.username,  
            guest_email=guest.email,
            check_in=booking.checkin_date,
            check_out=booking.checkout_date,
            is_active=booking.is_active
        ))

    return response_list
        