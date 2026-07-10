from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.models import Itinerary, ItineraryDay, User
from app.schemas import (
    ItineraryResponse,
    ItineraryDetailResponse,
    ItineraryCreate,
    ItineraryUpdate,
    ItineraryDayCreate,
    ItineraryDayResponse,
)
from app.auth import get_current_active_user
from app.utils.itinerary_generator import (
    generate_itinerary_days,
    optimize_route,
    estimate_budget
)

router = APIRouter()


# ==================== Create Itinerary ====================
@router.post("", response_model=ItineraryDetailResponse, status_code=status.HTTP_201_CREATED)
async def create_itinerary(
    itinerary_data: ItineraryCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    새로운 여행 계획 생성

    - **title**: 여행 계획명 (예: "2026 여름 가족 여행")
    - **departure_city**: 출발지 (예: "서울")
    - **start_date**: 출발 날짜
    - **end_date**: 귀국 날짜
    - **travel_theme**: 여행 테마 (couple, family, solo, friends)
    - **description**: 설명 (선택사항)
    - **budget_allocated**: 예산 (선택사항)
    """
    # 여행 기간 검증
    if itinerary_data.end_date <= itinerary_data.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="귀국 날짜가 출발 날짜보다 이후여야 합니다."
        )

    # 새 여행 계획 생성
    new_itinerary = Itinerary(
        user_id=current_user.id,
        **itinerary_data.dict()
    )

    db.add(new_itinerary)
    db.commit()
    db.refresh(new_itinerary)

    return new_itinerary


# ==================== Get My Itineraries ====================
@router.get("", response_model=List[ItineraryResponse])
async def get_my_itineraries(
    current_user: User = Depends(get_current_active_user),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    사용자의 여행 계획 목록 조회
    """
    itineraries = db.query(Itinerary).filter(
        Itinerary.user_id == current_user.id,
        Itinerary.is_active == True
    ).order_by(Itinerary.created_at.desc()).offset(skip).limit(limit).all()

    return itineraries


# ==================== Get Itinerary Detail ====================
@router.get("/{itinerary_id}", response_model=ItineraryDetailResponse)
async def get_itinerary_detail(
    itinerary_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    여행 계획 상세 정보 조회 (일정 + 예산 포함)
    """
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == itinerary_id,
        Itinerary.user_id == current_user.id,
        Itinerary.is_active == True
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행 계획을 찾을 수 없습니다."
        )

    return itinerary


# ==================== Generate Itinerary Days ====================
@router.post("/{itinerary_id}/generate-days")
async def generate_itinerary_days_endpoint(
    itinerary_id: int,
    destination_ids: List[int] = Query(..., description="여행지 ID 리스트"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    여행 일정 자동 생성

    사용자가 선택한 여행지들의 방문 순서를 최적화하고,
    각 날짜별로 추천 활동을 생성합니다.

    - **destination_ids**: 여행지 ID 리스트 (예: [1, 3, 5])
    """
    # 여행 계획 조회
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행 계획을 찾을 수 없습니다."
        )

    # 기존 일정 삭제
    db.query(ItineraryDay).filter(
        ItineraryDay.itinerary_id == itinerary_id
    ).delete()

    # 사용자 프로필에서 선호 활동 조회
    from app.models import UserProfile
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    preferred_activities = profile.preferred_activities if profile else None

    # 여행 일정 자동 생성
    itinerary_days_data = generate_itinerary_days(
        db=db,
        start_date=itinerary.start_date,
        end_date=itinerary.end_date,
        departure_city=itinerary.departure_city,
        destination_ids=destination_ids,
        preferred_activities=preferred_activities
    )

    # 생성된 일정 저장
    for day_data in itinerary_days_data:
        itinerary_day = ItineraryDay(
            itinerary_id=itinerary_id,
            **day_data.dict()
        )
        db.add(itinerary_day)

    db.commit()

    return {
        "message": f"{len(itinerary_days_data)}개의 일정이 생성되었습니다.",
        "total_days": len(itinerary_days_data),
        "itinerary_id": itinerary_id
    }


# ==================== Get Itinerary Days ====================
@router.get("/{itinerary_id}/days", response_model=List[ItineraryDayResponse])
async def get_itinerary_days(
    itinerary_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    여행 계획의 일정 조회
    """
    # 여행 계획 소유 확인
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행 계획을 찾을 수 없습니다."
        )

    # 일정 조회
    days = db.query(ItineraryDay).filter(
        ItineraryDay.itinerary_id == itinerary_id
    ).order_by(ItineraryDay.day_number).all()

    return days


# ==================== Add Activity to Day ====================
@router.post("/{itinerary_id}/days/{day_number}/activities")
async def add_activity_to_day(
    itinerary_id: int,
    day_number: int,
    activity_data: dict,  # time, place, duration, notes
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    특정 날짜에 활동 추가

    요청 본문:
    ```json
    {
      "time": "15:00",
      "place": "박물관",
      "duration": 120,
      "notes": "현대미술관 방문"
    }
    ```
    """
    # 여행 계획 소유 확인
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행 계획을 찾을 수 없습니다."
        )

    # 해당 날짜의 일정 조회
    itinerary_day = db.query(ItineraryDay).filter(
        ItineraryDay.itinerary_id == itinerary_id,
        ItineraryDay.day_number == day_number
    ).first()

    if not itinerary_day:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 날짜의 일정을 찾을 수 없습니다."
        )

    # 활동 추가
    if not itinerary_day.activities:
        itinerary_day.activities = []

    itinerary_day.activities.append(activity_data)
    db.commit()

    return {
        "message": "활동이 추가되었습니다.",
        "itinerary_day": itinerary_day
    }


# ==================== Update Itinerary ====================
@router.put("/{itinerary_id}", response_model=ItineraryResponse)
async def update_itinerary(
    itinerary_id: int,
    itinerary_data: ItineraryUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    여행 계획 정보 수정
    """
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행 계획을 찾을 수 없습니다."
        )

    # 업데이트
    update_data = itinerary_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(itinerary, field, value)

    db.commit()
    db.refresh(itinerary)

    return itinerary


# ==================== Delete Itinerary ====================
@router.delete("/{itinerary_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_itinerary(
    itinerary_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    여행 계획 삭제 (소프트 딜리트)
    """
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행 계획을 찾을 수 없습니다."
        )

    itinerary.is_active = False
    db.commit()

    return {"message": "여행 계획이 삭제되었습니다."}


# ==================== Estimate Budget ====================
@router.get("/{itinerary_id}/budget-estimate", response_model=dict)
async def estimate_itinerary_budget(
    itinerary_id: int,
    budget_level: str = Query("standard", regex="^(budget|standard|luxury)$"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    여행 계획의 예산 추정

    - **budget_level**: budget (저), standard (중), luxury (고)
    """
    itinerary = db.query(Itinerary).filter(
        Itinerary.id == itinerary_id,
        Itinerary.user_id == current_user.id
    ).first()

    if not itinerary:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행 계획을 찾을 수 없습니다."
        )

    # 여행지 ID 추출
    itinerary_days = db.query(ItineraryDay).filter(
        ItineraryDay.itinerary_id == itinerary_id
    ).distinct(ItineraryDay.destination_id).all()

    destination_ids = [day.destination_id for day in itinerary_days]

    # 예산 추정
    total_days = (itinerary.end_date - itinerary.start_date).days + 1
    budget = estimate_budget(
        db=db,
        destination_ids=destination_ids,
        total_days=total_days,
        budget_level=budget_level
    )

    return budget


# ==================== Get Travel Statistics ====================
@router.get("/stats/overview", response_model=dict)
async def get_travel_stats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    사용자의 여행 계획 통계
    """
    total_itineraries = db.query(Itinerary).filter(
        Itinerary.user_id == current_user.id,
        Itinerary.is_active == True
    ).count()

    total_destinations = db.query(ItineraryDay).filter(
        ItineraryDay.itinerary_id.in_(
            db.query(Itinerary.id).filter(
                Itinerary.user_id == current_user.id
            )
        )
    ).distinct(ItineraryDay.destination_id).count()

    total_days = db.query(ItineraryDay).filter(
        ItineraryDay.itinerary_id.in_(
            db.query(Itinerary.id).filter(
                Itinerary.user_id == current_user.id
            )
        )
    ).count()

    return {
        "total_itineraries": total_itineraries,
        "total_destinations": total_destinations,
        "total_days_planned": total_days
    }
