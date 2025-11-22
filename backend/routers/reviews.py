from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import db_dependency
from models import Review, Booking, User, Hotel
from schemas import ReviewCreate, ReviewResponse
from auth import get_current_user
from datetime import date

router = APIRouter(
    prefix="/reviews", 
    tags=["reviews"]
    )

@router.post("/create", response_model=ReviewResponse)
def create_review(
    review_request: ReviewCreate, 
    db: db_dependency,
    current_user: User = Depends(get_current_user)
):
    # 1. 驗證這筆訂單是否真的屬於該使用者
    target_booking = db.query(Booking).filter(
        Booking.id == review_request.booking_id,
        Booking.user_id == current_user.id,
        Booking.hotel_id == review_request.hotel_id
    ).first()

    if not target_booking:
        raise HTTPException(status_code=400, detail="無效的訂單，您無法評論此飯店")

    # 2. (進階) 驗證是否已經退房 (入住完才能評)
    # if target_booking.checkout_date > date.today():
    #     raise HTTPException(status_code=400, detail="尚未完成入住，無法評論")

    # 3. 驗證是否重複評論 (一筆訂單只能評一次)
    existing_review = db.query(Review).filter(
        Review.booking_id == review_request.booking_id
    ).first()

    if existing_review:
        raise HTTPException(status_code=400, detail="您已經評論過此次入住了")

    # 4. 建立評論
    new_review = Review(
        user_id=current_user.id,
        hotel_id=review_request.hotel_id,
        booking_id=review_request.booking_id,
        rating=review_request.rating,
        comment=review_request.comment
    )

    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    
    # 為了符合 Response Schema，手動塞入 username
    return ReviewResponse(
        id=new_review.id,
        user_id=new_review.user_id,
        username=current_user.username, # 讓前端可以直接顯示名字
        rating=new_review.rating,
        comment=new_review.comment,
        reply=new_review.reply,
        created_at=new_review.created_at
    )

# 取得某間飯店的所有評論
@router.get("/{hotel_id}", response_model=list[ReviewResponse])
def get_hotel_reviews(hotel_id: int, db: db_dependency):
    reviews = db.query(Review).filter(Review.hotel_id == hotel_id).all()
    
    # 這裡需要一點小處理，因為 Review 表裡只有 user_id，沒有 username
    results = []
    for review in reviews:
        results.append(ReviewResponse(
            id=review.id,
            user_id=review.user_id,
            username=review.user.username, # 利用 relationship 取得名字
            rating=review.rating,
            comment=review.comment,
            reply=review.reply,
            created_at=review.created_at
        ))
        
    return results