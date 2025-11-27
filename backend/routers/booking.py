from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import and_
from auth import db_dependency
from models import Booking, Hotel, User,Owner
from schemas import BookingCreate, BookingResponse,OwnerBookingResponse
from auth import get_current_user,get_current_owner
from datetime import date

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
        