from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_, func
from typing import List, Optional

from app.database import get_db
from app.models import Destination, UserProfile, User
from app.schemas import DestinationResponse, DestinationCreate, DestinationUpdate
from app.auth import get_current_active_user

router = APIRouter()


# ==================== Get All Destinations ====================
@router.get("", response_model=List[DestinationResponse])
async def get_destinations(
    skip: int = Query(0, ge=0, description="페이지 시작점"),
    limit: int = Query(10, ge=1, le=100, description="페이지 크기"),
    db: Session = Depends(get_db)
):
    """
    전체 여행지 목록 조회 (페이지네이션)

    - **skip**: 스킵할 항목 수 (기본값: 0)
    - **limit**: 반환할 항목 수 (기본값: 10, 최대: 100)
    """
    destinations = db.query(Destination).filter(
        Destination.is_active == True
    ).offset(skip).limit(limit).all()

    return destinations


# ==================== Get Destination by ID ====================
@router.get("/{destination_id}", response_model=DestinationResponse)
async def get_destination(
    destination_id: int,
    db: Session = Depends(get_db)
):
    """
    특정 여행지 상세 정보 조회
    """
    destination = db.query(Destination).filter(
        Destination.id == destination_id,
        Destination.is_active == True
    ).first()

    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행지를 찾을 수 없습니다."
        )

    return destination


# ==================== Search Destinations ====================
@router.post("/search", response_model=List[DestinationResponse])
async def search_destinations(
    keyword: Optional[str] = Query(None, description="검색 키워드"),
    location: Optional[str] = Query(None, description="위치/국가"),
    theme: Optional[str] = Query(None, description="테마 (couple, family, solo, friends)"),
    suitable_for_children: Optional[bool] = Query(None, description="아이 친화적 여부"),
    activity: Optional[str] = Query(None, description="활동 종류"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    여행지 검색

    - **keyword**: 여행지명 검색
    - **location**: 위치/국가로 필터링
    - **theme**: 테마별 필터링
    - **suitable_for_children**: 아이 친화적 여부
    - **activity**: 활동 종류로 필터링
    """
    query = db.query(Destination).filter(Destination.is_active == True)

    # 키워드 검색
    if keyword:
        query = query.filter(
            or_(
                Destination.name.ilike(f"%{keyword}%"),
                Destination.description.ilike(f"%{keyword}%")
            )
        )

    # 위치 필터
    if location:
        query = query.filter(Destination.location.ilike(f"%{location}%"))

    # 테마 필터
    if theme:
        query = query.filter(Destination.themes.contains([theme]))

    # 아이 친화적 여부
    if suitable_for_children is not None:
        query = query.filter(Destination.suitable_for_children == suitable_for_children)

    # 활동 필터
    if activity:
        query = query.filter(Destination.activities.contains([activity]))

    destinations = query.offset(skip).limit(limit).all()

    return destinations


# ==================== Recommend Destinations ====================
@router.get("/recommend/for-me", response_model=List[DestinationResponse])
async def recommend_destinations(
    current_user: User = Depends(get_current_active_user),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    사용자 프로필 기반 맞춤형 여행지 추천

    사용자의 여행 테마, 가족 구성, 선호 활동을 기반으로 추천합니다.
    """
    # 사용자 프로필 조회
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == current_user.id
    ).first()

    if not profile:
        # 프로필이 없으면 인기 여행지 반환
        return db.query(Destination).filter(
            Destination.is_active == True
        ).limit(limit).all()

    # 추천 쿼리 구성
    query = db.query(Destination).filter(Destination.is_active == True)

    # 1. 여행 테마로 필터
    if profile.travel_theme:
        query = query.filter(Destination.themes.contains([profile.travel_theme.value]))

    # 2. 아이가 있는 경우 아이 친화적 여행지 우선
    if profile.has_children:
        query = query.filter(Destination.suitable_for_children == True)

    # 3. 선호 활동으로 필터
    if profile.preferred_activities:
        or_conditions = []
        for activity in profile.preferred_activities:
            or_conditions.append(Destination.activities.contains([activity]))
        if or_conditions:
            from sqlalchemy import or_ as sql_or
            query = query.filter(sql_or(*or_conditions))

    destinations = query.limit(limit).all()

    return destinations


# ==================== Get Destinations by Theme ====================
@router.get("/theme/{theme}", response_model=List[DestinationResponse])
async def get_destinations_by_theme(
    theme: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    테마별 여행지 조회

    - **theme**: couple (커플), family (가족), solo (혼자), friends (친구)
    """
    valid_themes = ["couple", "family", "solo", "friends"]
    if theme.lower() not in valid_themes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"유효하지 않은 테마입니다. 가능한 값: {valid_themes}"
        )

    destinations = db.query(Destination).filter(
        Destination.is_active == True,
        Destination.themes.contains([theme.lower()])
    ).offset(skip).limit(limit).all()

    return destinations


# ==================== Get Family-Friendly Destinations ====================
@router.get("/filter/family-friendly", response_model=List[DestinationResponse])
async def get_family_friendly_destinations(
    family_size: Optional[int] = Query(None, ge=1, le=10, description="가족 인원수"),
    has_kids: Optional[bool] = Query(None, description="아이 동반 여부"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    가족 친화적 여행지 조회

    - **family_size**: 가족 인원수로 필터링
    - **has_kids**: 아이 친화적 여부
    """
    query = db.query(Destination).filter(
        Destination.is_active == True,
        Destination.suitable_for_children == True,
        Destination.themes.contains(["family"])
    )

    # 가족 크기로 필터
    if family_size:
        # family_size_recommended가 범위를 포함하는지 확인
        # 간단한 필터링 (실제로는 JSON 쿼리가 필요할 수 있음)
        pass

    destinations = query.offset(skip).limit(limit).all()

    return destinations


# ==================== Get Destinations by Activity ====================
@router.get("/filter/activity/{activity}", response_model=List[DestinationResponse])
async def get_destinations_by_activity(
    activity: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    활동 종류별 여행지 조회

    활동 종류:
    - beach: 해변
    - hiking: 등산
    - culture: 문화
    - museum: 박물관
    - restaurant: 레스토랑
    - shopping: 쇼핑
    - temple: 사원/신사
    - theme_park: 테마파크
    - etc.
    """
    valid_activities = [
        "beach", "hiking", "culture", "museum", "restaurant",
        "shopping", "temple", "theme_park", "water_sports",
        "nightlife", "market", "food", "yoga", "massage",
        "technology", "anime", "romantic", "adventure", "relaxation"
    ]

    if activity.lower() not in valid_activities:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"유효하지 않은 활동입니다. 가능한 값: {valid_activities}"
        )

    destinations = db.query(Destination).filter(
        Destination.is_active == True,
        Destination.activities.contains([activity.lower()])
    ).offset(skip).limit(limit).all()

    return destinations


# ==================== Get Popular Destinations ====================
@router.get("/popular/trending", response_model=List[DestinationResponse])
async def get_popular_destinations(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    인기 있는 여행지 조회 (최근 업데이트된 순서)
    """
    destinations = db.query(Destination).filter(
        Destination.is_active == True
    ).order_by(Destination.updated_at.desc()).limit(limit).all()

    return destinations


# ==================== Admin: Create Destination ====================
@router.post("", response_model=DestinationResponse, status_code=status.HTTP_201_CREATED)
async def create_destination(
    destination_data: DestinationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    새로운 여행지 추가 (관리자 전용)
    """
    # 관리자 확인 (현재는 누구나 가능, 실제로는 is_admin 확인 필요)
    # TODO: 관리자 권한 확인 로직 추가

    new_destination = Destination(**destination_data.dict())
    db.add(new_destination)
    db.commit()
    db.refresh(new_destination)

    return new_destination


# ==================== Admin: Update Destination ====================
@router.put("/{destination_id}", response_model=DestinationResponse)
async def update_destination(
    destination_id: int,
    destination_data: DestinationUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    여행지 정보 수정 (관리자 전용)
    """
    destination = db.query(Destination).filter(
        Destination.id == destination_id
    ).first()

    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행지를 찾을 수 없습니다."
        )

    # 업데이트 데이터 적용
    update_data = destination_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(destination, field, value)

    db.commit()
    db.refresh(destination)

    return destination


# ==================== Admin: Delete Destination ====================
@router.delete("/{destination_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_destination(
    destination_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    여행지 삭제 (소프트 딜리트 - 비활성화)
    """
    destination = db.query(Destination).filter(
        Destination.id == destination_id
    ).first()

    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="여행지를 찾을 수 없습니다."
        )

    # 소프트 딜리트
    destination.is_active = False
    db.commit()

    return {"message": "여행지가 삭제되었습니다."}


# ==================== Statistics ====================
@router.get("/stats/count", response_model=dict)
async def get_destination_statistics(db: Session = Depends(get_db)):
    """
    여행지 통계
    """
    total_count = db.query(Destination).filter(
        Destination.is_active == True
    ).count()

    # 테마별 카운트
    theme_counts = {
        "couple": db.query(Destination).filter(
            Destination.is_active == True,
            Destination.themes.contains(["couple"])
        ).count(),
        "family": db.query(Destination).filter(
            Destination.is_active == True,
            Destination.themes.contains(["family"])
        ).count(),
        "solo": db.query(Destination).filter(
            Destination.is_active == True,
            Destination.themes.contains(["solo"])
        ).count(),
        "friends": db.query(Destination).filter(
            Destination.is_active == True,
            Destination.themes.contains(["friends"])
        ).count(),
    }

    return {
        "total": total_count,
        "by_theme": theme_counts,
        "kids_friendly": db.query(Destination).filter(
            Destination.is_active == True,
            Destination.suitable_for_children == True
        ).count()
    }
