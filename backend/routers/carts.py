from datetime import datetime, date
from models import User,Hotel,Booking
from fastapi import APIRouter, Depends, HTTPException, status
from auth import get_current_user, db_dependency
from sqlalchemy.orm import Session
from schemas import CartItemResponse,CartAddRequest

router = APIRouter(
    prefix="/carts",
    tags=["carts"]
)

@router.post("/add/{hotel_id}", status_code=status.HTTP_201_CREATED)
async def add_hotel_to_cart(hotel_id: int, 
    cart_request: CartAddRequest, # 🔥 新增：接收日期參數
    db: db_dependency,
    user: User = Depends(get_current_user)
):
    
    hotel=db.query(Hotel).filter(Hotel.id==hotel.id).first()
    if not hotel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="hotel not found")
    hotel=db.query(Hotel).filter(Hotel.id==hotel_id).first()
    
    if not hotel.is_activate:
        raise HTTPException(status_code=400, detail="此飯店已下架，無法預訂")
    
    #🔥 資料驗證：退房日必須晚於入住日
    if cart_request.checkout_date <= cart_request.checkin_date:
        raise HTTPException(status_code=400, detail="退房日期必須晚於入住日期")
    
    existing_cart_item = db.query(Booking).filter(
        Booking.user_id == user.id,
        Booking.hotel_id == hotel_id,
        Booking.status == "CART", # 只檢查購物車裡的
        Booking.checkin_date == str(cart_request.checkin_date), # 比對日期
        Booking.checkout_date == str(cart_request.checkout_date)
    ).first()
    
    if existing_cart_item:
        raise HTTPException(status_code=400,detail="已於你的購物車")
    
    new_cart_item=Booking(
        user_id=user.id,
        hotel_id=hotel.id,
        checkin_date=str(cart_request.checkin_date),   # 轉成字串存入
        checkout_date=str(cart_request.checkout_date), # 轉成字串存入
        status="CART",  # ✅ 關鍵：標記為購物車項目
        is_active=True
    )
    db.add(new_cart_item)
    db.commit()

    return {"message": "成功加入購物車"}

#paid API
@router.post("/checkout", status_code=status.HTTP_200_OK)
async def checkout(
    db: db_dependency,
    user: User = Depends(get_current_user)
):
    # 1. 找出購物車裡所有的項目 (status='CART')
    # 建議加上日期限制 (>= today)，避免幫過去過期的購物車項目結帳
    today_str = date.today().strftime("%Y-%m-%d")
    
    cart_items = db.query(Booking).filter(
        Booking.user_id == user.id,
        Booking.status == "CART",
        Booking.is_active == True,
        Booking.checkin_date >= today_str
    ).all()

    if not cart_items:
        raise HTTPException(status_code=400, detail="購物車是空的，無法結帳")
    
    for item in cart_items:
        # 透過關聯取得飯店資訊
        hotel = item.hotel_rel 
        
        # 如果飯店被刪除了 (is_activate = False)
        if not hotel or not hotel.is_activate:
            # 做法 A: 直接報錯，叫他去整理購物車 (較嚴格)
            raise HTTPException(
                status_code=400, 
                detail=f"飯店 '{hotel.hotel_name}' 已下架，請將其移出購物車後再結帳"
            )

    # 2. 🔥 核心動作：狀態轉換 (CART -> PAID)
    for booking in cart_items:
        booking.status = "PAID"
        # 未來如果接金流 (綠界/Stripe)，會在這裡處理付款驗證
    
    # 3. 存檔
    db.commit()

    return {"message": "結帳成功", "count": len(cart_items)}

@router.get("/", status_code=status.HTTP_200_OK,response_model=list[CartItemResponse])
async def get_user_cart(db: db_dependency,
                        user: User = Depends(get_current_user)):
    today_str=date.today().strftime("%Y-%m-%d")
    user_bookings=db.query(Booking).filter(
        Booking.user_id==user.id,
        Booking.checkin_date>=today_str,
        Booking.status=="CART",
        Booking.is_active==True
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

@router.delete("/delete/{booking_id}", status_code=status.HTTP_200_OK)
async def remove_hotel_from_cart(db: db_dependency,
                                booking_id: int, 
                                 user: User = Depends(get_current_user)):
    
    booking=db.query(Booking).filter(
        Booking.id==booking_id,
        Booking.user_id==user.id
    ).first()

    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="booking not found")
    
    hotel=booking.hotel_rel

    db_user = db.query(User).filter(User.id == user.id).first()
    if hotel and db_user and (hotel in db_user.carts):
        db_user.carts.remove(hotel)

    db.delete(booking)
    db.commit()
    
    return None






