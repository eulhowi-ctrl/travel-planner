"""
여행 일정 자동 생성 유틸리티
"""

from datetime import datetime, timedelta
from typing import List, Dict, Tuple
import random
from sqlalchemy.orm import Session

from app.models import Destination, ItineraryDay, LongDistanceTransportation
from app.schemas import ItineraryDayCreate, ActivityItem


def generate_itinerary_days(
    db: Session,
    start_date: datetime,
    end_date: datetime,
    departure_city: str,
    destination_ids: List[int],
    preferred_activities: List[str] = None
) -> List[ItineraryDayCreate]:
    """
    여행 일정 자동 생성

    Args:
        db: 데이터베이스 세션
        start_date: 출발 날짜
        end_date: 귀국 날짜
        departure_city: 출발지 도시
        destination_ids: 여행지 ID 리스트
        preferred_activities: 선호하는 활동 리스트

    Returns:
        생성된 여행 일정 리스트
    """
    # 여행 일수 계산
    total_days = (end_date - start_date).days + 1

    # 각 여행지별 일수 배분 (총 일수를 여행지 수로 나누기, 최소 1일)
    days_per_destination = max(1, (total_days - 2) // len(destination_ids)) if destination_ids else total_days

    # 여행지 정보 조회
    destinations = db.query(Destination).filter(
        Destination.id.in_(destination_ids),
        Destination.is_active == True
    ).all()

    if not destinations:
        return []

    itinerary_days = []
    current_date = start_date + timedelta(days=1)  # 첫 날은 이동 날짜
    day_number = 1

    # 첫 날: 출발지에서 첫 여행지로 이동
    first_destination = destinations[0]
    itinerary_days.append(
        ItineraryDayCreate(
            day_number=day_number,
            destination_id=first_destination.id,
            date=current_date,
            activities=_generate_activities_for_day(first_destination, preferred_activities, "arrival"),
            notes=f"{departure_city}에서 {first_destination.name}으로 출발"
        )
    )

    current_date += timedelta(days=1)
    day_number += 1

    # 중간 여행지들
    for i, destination in enumerate(destinations[1:], 1):
        for _ in range(days_per_destination):
            if current_date >= end_date:
                break

            itinerary_days.append(
                ItineraryDayCreate(
                    day_number=day_number,
                    destination_id=destination.id,
                    date=current_date,
                    activities=_generate_activities_for_day(destination, preferred_activities, "regular"),
                    notes=f"{destination.name} 관광"
                )
            )

            current_date += timedelta(days=1)
            day_number += 1

        if current_date >= end_date:
            break

    # 마지막 날: 귀국
    if itinerary_days:
        last_day = itinerary_days[-1]
        last_day.notes = f"{last_day.notes} (귀국 날짜)"

    return itinerary_days


def _generate_activities_for_day(
    destination: Destination,
    preferred_activities: List[str] = None,
    day_type: str = "regular"
) -> List[ActivityItem]:
    """
    하루 일정에 맞는 활동 생성

    Args:
        destination: 여행지 정보
        preferred_activities: 선호하는 활동
        day_type: 날짜 유형 (arrival/regular/departure)

    Returns:
        활동 리스트
    """
    activities = []

    if day_type == "arrival":
        # 도착 날: 체크인, 가벼운 활동
        activities = [
            ActivityItem(
                time="14:00",
                place="숙박지 체크인",
                duration=60,
                notes="짐 정리 및 휴식"
            ),
            ActivityItem(
                time="17:00",
                place=f"{destination.name} 주변 산책",
                duration=90,
                notes="현지 분위기 감상"
            )
        ]
    elif day_type == "departure":
        # 출발 날: 아침 활동, 체크아웃
        activities = [
            ActivityItem(
                time="09:00",
                place="조식",
                duration=60,
                notes="호텔 조식"
            ),
            ActivityItem(
                time="11:00",
                place="숙박지 체크아웃",
                duration=30,
                notes="짐 정리"
            ),
            ActivityItem(
                time="13:00",
                place="공항 출발",
                duration=180,
                notes="귀국 항공편"
            )
        ]
    else:
        # 일반 날: 다양한 활동
        activity_times = ["09:00", "11:30", "14:00", "17:00"]
        available_activities = destination.activities[:4] if destination.activities else []

        # 선호 활동과 매칭
        if preferred_activities:
            preferred_available = [
                a for a in available_activities if a in preferred_activities
            ]
            if preferred_available:
                available_activities = preferred_available + [
                    a for a in available_activities if a not in preferred_available
                ]

        for i, (time, activity_name) in enumerate(zip(activity_times, available_activities)):
            activity_display_name = _get_activity_display_name(activity_name, destination.name)
            activities.append(
                ActivityItem(
                    time=time,
                    place=activity_display_name,
                    duration=90,
                    notes=_get_activity_description(activity_name)
                )
            )

    return activities


def _get_activity_display_name(activity: str, destination_name: str) -> str:
    """활동명 변환"""
    activity_names = {
        "beach": "해변 방문",
        "hiking": "등산/트레킹",
        "culture": "문화 관광",
        "museum": "박물관 방문",
        "restaurant": "현지 음식점",
        "shopping": "쇼핑",
        "temple": "사원/신사 방문",
        "theme_park": "테마파크",
        "water_sports": "수상 스포츠",
        "nightlife": "야생활",
        "market": "전통 시장",
        "food": "음식 투어",
        "yoga": "요가",
        "massage": "스파/마사지",
        "technology": "기술 박물관",
        "anime": "애니메 성지",
        "romantic": "로맨틱한 장소",
        "adventure": "모험 활동",
        "relaxation": "휴식",
    }
    return activity_names.get(activity, f"{destination_name} {activity}")


def _get_activity_description(activity: str) -> str:
    """활동 설명"""
    descriptions = {
        "beach": "아름다운 해변에서 휴식",
        "hiking": "자연 속에서 등산/트레킹",
        "culture": "현지 문화와 역사 체험",
        "museum": "미술관과 박물관 관람",
        "restaurant": "현지 특색 음식 맛보기",
        "shopping": "기념품 및 쇼핑",
        "temple": "종교 유적지 방문",
        "theme_park": "테마파크 즐기기",
        "water_sports": "수상 활동 체험",
        "nightlife": "현지 클럽/바 경험",
        "market": "전통 시장 구경",
        "food": "음식 투어 및 시식",
        "yoga": "요가 클래스",
        "massage": "전통 마사지/스파",
        "technology": "기술 박물관 방문",
        "anime": "애니메 성지 순례",
        "romantic": "연인과 함께 시간 보내기",
        "adventure": "모험적인 활동 체험",
        "relaxation": "느긋하게 휴식하기",
    }
    return descriptions.get(activity, "흥미로운 활동")


def optimize_route(
    db: Session,
    destination_ids: List[int],
    start_point: str
) -> List[int]:
    """
    여행지 방문 순서 최적화 (간단한 알고리즘)

    현재는 입력된 순서 그대로 반환
    실제로는 거리 기반 최적화(TSP) 필요

    Args:
        db: 데이터베이스 세션
        destination_ids: 여행지 ID 리스트
        start_point: 출발점

    Returns:
        최적화된 여행지 ID 순서
    """
    # TODO: 거리 기반 최적화 (TSP - Traveling Salesman Problem)
    # 현재는 입력 순서 그대로 반환
    return destination_ids


def estimate_budget(
    db: Session,
    destination_ids: List[int],
    total_days: int,
    budget_level: str = "standard"
) -> Dict[str, float]:
    """
    예산 추정

    Args:
        db: 데이터베이스 세션
        destination_ids: 여행지 ID 리스트
        total_days: 여행 일수
        budget_level: 예산 수준 (budget/standard/luxury)

    Returns:
        예산 추정치
    """
    # 일일 예산 (통화: KRW)
    daily_budgets = {
        "budget": 100000,      # 10만원
        "standard": 200000,    # 20만원
        "luxury": 400000       # 40만원
    }

    daily_budget = daily_budgets.get(budget_level, 200000)

    # 기본 예산 계산
    accommodation_cost = daily_budget * 0.4 * total_days  # 40%
    food_cost = daily_budget * 0.3 * total_days  # 30%
    activity_cost = daily_budget * 0.2 * total_days  # 20%
    transport_cost = 100000 * len(destination_ids)  # 교통비

    total_estimated = accommodation_cost + food_cost + activity_cost + transport_cost

    return {
        "total_estimated": total_estimated,
        "accommodation": accommodation_cost,
        "food": food_cost,
        "activities": activity_cost,
        "transport": transport_cost,
        "daily_average": daily_budget,
        "total_days": total_days
    }


if __name__ == "__main__":
    # 테스트 코드
    from app.database import SessionLocal

    db = SessionLocal()

    # 샘플 데이터로 테스트
    start = datetime(2026, 8, 1)
    end = datetime(2026, 8, 7)
    days = generate_itinerary_days(
        db=db,
        start_date=start,
        end_date=end,
        departure_city="서울",
        destination_ids=[1, 2],
        preferred_activities=["beach", "culture"]
    )

    print(f"Generated {len(days)} itinerary days:")
    for day in days:
        print(f"  Day {day.day_number}: {day.date.strftime('%Y-%m-%d')} - Destination {day.destination_id}")
        for activity in day.activities:
            print(f"    - {activity.time}: {activity.place} ({activity.duration}분)")

    budget = estimate_budget(db, [1, 2], 7, "standard")
    print(f"\nEstimated Budget: {budget['total_estimated']:,.0f} KRW")

    db.close()
