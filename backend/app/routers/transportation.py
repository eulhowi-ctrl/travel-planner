from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.database import get_db
from app.models import LongDistanceTransportation, LocalTransportation, Destination
from app.schemas import (
    LongDistanceTransportationResponse,
    LongDistanceTransportationCreate,
    LongDistanceTransportationBase,
    LocalTransportationResponse,
    LocalTransportationCreate,
    LocalTransportationBase,
)
from app.auth import get_current_active_user
from app.models import User

router = APIRouter()


# ==================== Long-Distance Transportation ====================

@router.get("/long-distance", response_model=List[LongDistanceTransportationResponse])
async def get_long_distance_transports(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    전국 장거리 교통편 목록 조회

    **교통 수단:**
    - flight: 항공편
    - train: 기차
    - bus: 버스
    - ferry: 페리
    """
    transports = db.query(LongDistanceTransportation).offset(skip).limit(limit).all()
    return transports


@router.get("/long-distance/{transport_id}", response_model=LongDistanceTransportationResponse)
async def get_long_distance_transport_detail(
    transport_id: int,
    db: Session = Depends(get_db)
):
    """
    장거리 교통편 상세 정보 조회
    """
    transport = db.query(LongDistanceTransportation).filter(
        LongDistanceTransportation.id == transport_id
    ).first()

    if not transport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="교통편을 찾을 수 없습니다."
        )

    return transport


@router.post("/long-distance/search", response_model=List[LongDistanceTransportationResponse])
async def search_long_distance_transports(
    departure_city: Optional[str] = Query(None, description="출발 도시"),
    arrival_city: Optional[str] = Query(None, description="도착 도시"),
    transport_type: Optional[str] = Query(None, description="교통 수단 (flight/train/bus/ferry)"),
    min_price: Optional[float] = Query(None, ge=0, description="최소 가격"),
    max_price: Optional[float] = Query(None, ge=0, description="최대 가격"),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    장거리 교통편 검색

    **검색 조건:**
    - departure_city: 출발 도시 (예: "서울")
    - arrival_city: 도착 도시 (예: "제주")
    - transport_type: 교통 수단 (flight/train/bus/ferry)
    - min_price/max_price: 가격 범위

    **예시:**
    ```
    /api/v1/transportation/long-distance/search?departure_city=서울&arrival_city=제주&transport_type=flight
    ```
    """
    query = db.query(LongDistanceTransportation)

    if departure_city:
        query = query.filter(LongDistanceTransportation.departure_city == departure_city)

    if arrival_city:
        query = query.filter(LongDistanceTransportation.arrival_city == arrival_city)

    if transport_type:
        query = query.filter(LongDistanceTransportation.type == transport_type)

    if min_price is not None:
        query = query.filter(LongDistanceTransportation.price >= min_price)

    if max_price is not None:
        query = query.filter(LongDistanceTransportation.price <= max_price)

    transports = query.order_by(LongDistanceTransportation.price).limit(limit).all()
    return transports


@router.post("/long-distance", response_model=LongDistanceTransportationResponse, status_code=status.HTTP_201_CREATED)
async def create_long_distance_transport(
    transport_data: LongDistanceTransportationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    장거리 교통편 추가 (관리자)

    예시:
    ```json
    {
      "type": "flight",
      "departure_city": "서울",
      "arrival_city": "제주",
      "departure_time": "2026-07-15T14:00:00",
      "arrival_time": "2026-07-15T15:30:00",
      "price": 85000,
      "currency": "KRW",
      "provider": "Korean Air",
      "provider_code": "KE1234",
      "booking_methods": [
        {
          "platform": "Official Website",
          "url": "https://www.koreanair.com",
          "how_to": "Direct booking"
        }
      ],
      "directions": "서울 김포공항 → 제주 국제공항"
    }
    ```
    """
    # Check admin status (optional - for now allow all users)
    # In production, add role-based access control

    new_transport = LongDistanceTransportation(
        **transport_data.dict()
    )

    db.add(new_transport)
    db.commit()
    db.refresh(new_transport)

    return new_transport


@router.put("/long-distance/{transport_id}", response_model=LongDistanceTransportationResponse)
async def update_long_distance_transport(
    transport_id: int,
    transport_data: LongDistanceTransportationBase,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    장거리 교통편 수정 (관리자)
    """
    transport = db.query(LongDistanceTransportation).filter(
        LongDistanceTransportation.id == transport_id
    ).first()

    if not transport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="교통편을 찾을 수 없습니다."
        )

    update_data = transport_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(transport, field, value)

    db.commit()
    db.refresh(transport)

    return transport


@router.delete("/long-distance/{transport_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_long_distance_transport(
    transport_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    장거리 교통편 삭제 (관리자)
    """
    transport = db.query(LongDistanceTransportation).filter(
        LongDistanceTransportation.id == transport_id
    ).first()

    if not transport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="교통편을 찾을 수 없습니다."
        )

    db.delete(transport)
    db.commit()

    return {"message": "교통편이 삭제되었습니다."}


# ==================== Local Transportation ====================

@router.get("/local", response_model=List[LocalTransportationResponse])
async def get_local_transports(
    destination_id: Optional[int] = Query(None, description="여행지 ID"),
    city: Optional[str] = Query(None, description="도시명"),
    transport_type: Optional[str] = Query(None, description="교통 수단"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    도시 지역 교통편 목록 조회

    **교통 수단:**
    - bus: 버스
    - subway: 지하철
    - taxi: 택시
    - bike: 자전거
    - tram: 트램
    """
    query = db.query(LocalTransportation)

    if destination_id:
        query = query.filter(LocalTransportation.destination_id == destination_id)

    if city:
        query = query.filter(LocalTransportation.city == city)

    if transport_type:
        query = query.filter(LocalTransportation.transport_type == transport_type)

    transports = query.offset(skip).limit(limit).all()
    return transports


@router.get("/local/{transport_id}", response_model=LocalTransportationResponse)
async def get_local_transport_detail(
    transport_id: int,
    db: Session = Depends(get_db)
):
    """
    지역 교통편 상세 정보 조회
    """
    transport = db.query(LocalTransportation).filter(
        LocalTransportation.id == transport_id
    ).first()

    if not transport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="교통편을 찾을 수 없습니다."
        )

    return transport


@router.post("/local/search", response_model=List[LocalTransportationResponse])
async def search_local_transports(
    city: Optional[str] = Query(None, description="도시명"),
    destination_id: Optional[int] = Query(None, description="여행지 ID"),
    transport_type: Optional[str] = Query(None, description="교통 수단"),
    max_fare: Optional[float] = Query(None, ge=0, description="최대 요금"),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    지역 교통편 검색

    **검색 조건:**
    - city: 도시명 (예: "제주")
    - destination_id: 여행지 ID
    - transport_type: 교통 수단 (bus/subway/taxi/bike/tram)
    - max_fare: 최대 요금

    **예시:**
    ```
    /api/v1/transportation/local/search?city=제주&transport_type=bus
    ```
    """
    query = db.query(LocalTransportation)

    if city:
        query = query.filter(LocalTransportation.city == city)

    if destination_id:
        query = query.filter(LocalTransportation.destination_id == destination_id)

    if transport_type:
        query = query.filter(LocalTransportation.transport_type == transport_type)

    if max_fare is not None:
        query = query.filter(LocalTransportation.fare <= max_fare)

    transports = query.order_by(LocalTransportation.fare).limit(limit).all()
    return transports


@router.post("/local", response_model=LocalTransportationResponse, status_code=status.HTTP_201_CREATED)
async def create_local_transport(
    transport_data: LocalTransportationCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    지역 교통편 추가 (관리자)

    예시:
    ```json
    {
      "destination_id": 1,
      "transport_type": "bus",
      "city": "제주",
      "route_number": "100",
      "fare": 2500,
      "currency": "KRW",
      "frequency": "10-15분 간격",
      "operating_hours": {
        "start": "06:00",
        "end": "23:00"
      },
      "payment_methods": ["cash", "card"],
      "useful_links": {
        "timetable": "https://example.com"
      }
    }
    ```
    """
    # Validate destination exists
    destination = db.query(Destination).filter(
        Destination.id == transport_data.destination_id
    ).first()

    if not destination:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 여행지를 찾을 수 없습니다."
        )

    new_transport = LocalTransportation(
        **transport_data.dict()
    )

    db.add(new_transport)
    db.commit()
    db.refresh(new_transport)

    return new_transport


@router.put("/local/{transport_id}", response_model=LocalTransportationResponse)
async def update_local_transport(
    transport_id: int,
    transport_data: LocalTransportationBase,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    지역 교통편 수정 (관리자)
    """
    transport = db.query(LocalTransportation).filter(
        LocalTransportation.id == transport_id
    ).first()

    if not transport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="교통편을 찾을 수 없습니다."
        )

    update_data = transport_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(transport, field, value)

    db.commit()
    db.refresh(transport)

    return transport


@router.delete("/local/{transport_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_local_transport(
    transport_id: int,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    지역 교통편 삭제 (관리자)
    """
    transport = db.query(LocalTransportation).filter(
        LocalTransportation.id == transport_id
    ).first()

    if not transport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="교통편을 찾을 수 없습니다."
        )

    db.delete(transport)
    db.commit()

    return {"message": "교통편이 삭제되었습니다."}


# ==================== Transportation Statistics ====================

@router.get("/stats/routes", response_model=dict)
async def get_transportation_stats(
    db: Session = Depends(get_db)
):
    """
    교통편 통계
    """
    long_distance_count = db.query(LongDistanceTransportation).count()
    local_transport_count = db.query(LocalTransportation).count()

    # Routes by type
    from sqlalchemy import func
    route_types = db.query(
        LongDistanceTransportation.type,
        func.count(LongDistanceTransportation.id).label("count")
    ).group_by(LongDistanceTransportation.type).all()

    # Cities covered
    cities = db.query(LocalTransportation.city).distinct().count()

    return {
        "total_long_distance": long_distance_count,
        "total_local_transports": local_transport_count,
        "total_cities_covered": cities,
        "routes_by_type": {route_type: count for route_type, count in route_types}
    }


# ==================== Transportation Tips ====================

@router.get("/tips", response_model=dict)
async def get_transportation_tips():
    """
    교통편 이용 팁
    """
    return {
        "long_distance": [
            "비행기는 출발 2시간 전에 공항에 도착하세요",
            "미리 발권하면 수수료를 절약할 수 있습니다",
            "인천-제주 항공편은 한 시간 소요됩니다",
            "기차는 버스보다 편안하지만 더 비쌉니다",
            "야간 버스는 숙박비를 절약할 수 있습니다"
        ],
        "local_transport": [
            "현지 교통카드(T-money 등)를 구입하면 요금이 저렴합니다",
            "지하철은 버스보다 빠르고 안정적입니다",
            "택시는 야간에 할증료가 추가됩니다",
            "대중교통 앱을 미리 다운로드하세요",
            "관광지 주변은 교통이 복잡하므로 시간 여유를 두세요"
        ],
        "booking_tips": [
            "여름/겨울 성수기는 미리 예약하세요",
            "평일이 주말보다 저렴합니다",
            "다양한 플랫폼 가격을 비교하세요",
            "취소 정책을 확인하세요",
            "할인 프로모션을 활용하세요"
        ]
    }
