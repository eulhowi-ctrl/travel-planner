"""
여행지 샘플 데이터 생성 스크립트
"""

from sqlalchemy.orm import Session
from app.models import Destination, LongDistanceTransportation, LocalTransportation
from datetime import datetime, timedelta

# 샘플 여행지 데이터
SAMPLE_DESTINATIONS = [
    {
        "name": "제주도",
        "location": "대한민국",
        "country": "South Korea",
        "description": "한국의 아름다운 섬으로 해변, 산, 문화유산이 풍부합니다.",
        "latitude": 33.3688,
        "longitude": 126.5412,
        "themes": ["couple", "family", "kids-friendly", "beach"],
        "suitable_for_children": True,
        "family_size_recommended": {"min": 1, "max": 10},
        "activities": ["beach", "hiking", "water_sports", "restaurant", "museum", "theme_park"],
        "images": [
            "https://via.placeholder.com/400x300?text=Jeju+Beach",
            "https://via.placeholder.com/400x300?text=Jeju+Mountain"
        ],
        "useful_links": {
            "tourism_board": "https://www.visitjeju.net",
            "official_map": "https://map.jeju.go.kr",
            "hotels": ["https://agoda.com/jeju"],
            "restaurants": ["https://naver.me/jeju"]
        }
    },
    {
        "name": "서울",
        "location": "대한민국",
        "country": "South Korea",
        "description": "한국의 수도로 현대와 전통이 어우러진 대도시입니다.",
        "latitude": 37.5665,
        "longitude": 126.9780,
        "themes": ["couple", "family", "solo", "friends", "shopping"],
        "suitable_for_children": True,
        "family_size_recommended": {"min": 1, "max": 10},
        "activities": ["culture", "shopping", "restaurant", "museum", "nightlife", "temple"],
        "images": [
            "https://via.placeholder.com/400x300?text=Seoul+City",
            "https://via.placeholder.com/400x300?text=Seoul+Palace"
        ],
        "useful_links": {
            "tourism_board": "https://www.visitseoul.net",
            "official_map": "https://map.naver.com",
            "hotels": ["https://agoda.com/seoul"],
            "restaurants": ["https://naver.me/seoul"]
        }
    },
    {
        "name": "부산",
        "location": "대한민국",
        "country": "South Korea",
        "description": "해변 도시로 해산물 요리와 아름다운 항구가 특징입니다.",
        "latitude": 35.1796,
        "longitude": 129.0756,
        "themes": ["couple", "family", "kids-friendly", "beach", "food"],
        "suitable_for_children": True,
        "family_size_recommended": {"min": 1, "max": 8},
        "activities": ["beach", "seafood", "hiking", "temple", "market"],
        "images": [
            "https://via.placeholder.com/400x300?text=Busan+Beach",
            "https://via.placeholder.com/400x300?text=Busan+Harbor"
        ],
        "useful_links": {
            "tourism_board": "https://www.visitbusan.net",
            "official_map": "https://map.naver.com/busan",
            "hotels": ["https://agoda.com/busan"],
            "restaurants": ["https://naver.me/busan"]
        }
    },
    {
        "name": "도쿄",
        "location": "일본",
        "country": "Japan",
        "description": "일본의 수도로 전통과 미래 기술이 공존하는 도시입니다.",
        "latitude": 35.6762,
        "longitude": 139.6503,
        "themes": ["couple", "family", "solo", "friends", "shopping"],
        "suitable_for_children": True,
        "family_size_recommended": {"min": 1, "max": 10},
        "activities": ["culture", "shopping", "anime", "technology", "restaurant", "temple"],
        "images": [
            "https://via.placeholder.com/400x300?text=Tokyo+City",
            "https://via.placeholder.com/400x300?text=Tokyo+Tower"
        ],
        "useful_links": {
            "tourism_board": "https://www.gotokyo.org",
            "official_map": "https://maps.google.com/tokyo",
            "hotels": ["https://agoda.com/tokyo"],
            "restaurants": ["https://tabelog.com"]
        }
    },
    {
        "name": "오사카",
        "location": "일본",
        "country": "Japan",
        "description": "일본의 요리 중심지로 맛있는 음식과 쇼핑이 유명합니다.",
        "latitude": 34.6937,
        "longitude": 135.5023,
        "themes": ["couple", "family", "food", "friends", "shopping"],
        "suitable_for_children": True,
        "family_size_recommended": {"min": 1, "max": 8},
        "activities": ["food", "shopping", "theme_park", "castle", "nightlife"],
        "images": [
            "https://via.placeholder.com/400x300?text=Osaka+Food",
            "https://via.placeholder.com/400x300?text=Osaka+Castle"
        ],
        "useful_links": {
            "tourism_board": "https://www.osaka-info.jp",
            "official_map": "https://maps.google.com/osaka",
            "hotels": ["https://agoda.com/osaka"],
            "restaurants": ["https://tabelog.com"]
        }
    },
    {
        "name": "방콕",
        "location": "태국",
        "country": "Thailand",
        "description": "태국의 수도로 불교 사원, 야시장, 태국 음식이 풍부합니다.",
        "latitude": 13.7563,
        "longitude": 100.5018,
        "themes": ["couple", "family", "budget", "adventure", "food"],
        "suitable_for_children": True,
        "family_size_recommended": {"min": 1, "max": 10},
        "activities": ["temple", "market", "food", "shopping", "water_sports", "massage"],
        "images": [
            "https://via.placeholder.com/400x300?text=Bangkok+Temple",
            "https://via.placeholder.com/400x300?text=Bangkok+Market"
        ],
        "useful_links": {
            "tourism_board": "https://www.thailand.go.th",
            "official_map": "https://maps.google.com/bangkok",
            "hotels": ["https://agoda.com/bangkok"],
            "restaurants": ["https://www.tripadvisor.com/bangkok"]
        }
    },
    {
        "name": "싱가포르",
        "location": "싱가포르",
        "country": "Singapore",
        "description": "현대적인 도시-국가로 쇼핑, 먹거리, 정원이 유명합니다.",
        "latitude": 1.3521,
        "longitude": 103.8198,
        "themes": ["couple", "family", "kids-friendly", "shopping", "modern"],
        "suitable_for_children": True,
        "family_size_recommended": {"min": 1, "max": 6},
        "activities": ["theme_park", "shopping", "garden", "restaurant", "technology"],
        "images": [
            "https://via.placeholder.com/400x300?text=Singapore+Marina",
            "https://via.placeholder.com/400x300?text=Singapore+Gardens"
        ],
        "useful_links": {
            "tourism_board": "https://www.visitsingapore.com",
            "official_map": "https://maps.google.com/singapore",
            "hotels": ["https://agoda.com/singapore"],
            "restaurants": ["https://www.tripadvisor.com/singapore"]
        }
    },
    {
        "name": "파리",
        "location": "프랑스",
        "country": "France",
        "description": "낭만의 도시로 미술관, 카페, 에펠탑이 유명합니다.",
        "latitude": 48.8566,
        "longitude": 2.3522,
        "themes": ["couple", "family", "culture", "romantic"],
        "suitable_for_children": True,
        "family_size_recommended": {"min": 2, "max": 6},
        "activities": ["museum", "culture", "restaurant", "shopping", "romantic"],
        "images": [
            "https://via.placeholder.com/400x300?text=Paris+Eiffel",
            "https://via.placeholder.com/400x300?text=Paris+Louvre"
        ],
        "useful_links": {
            "tourism_board": "https://en.parisinfo.com",
            "official_map": "https://maps.google.com/paris",
            "hotels": ["https://agoda.com/paris"],
            "restaurants": ["https://www.michelin.com"]
        }
    },
    {
        "name": "뉴욕",
        "location": "미국",
        "country": "USA",
        "description": "미국의 대표 도시로 브로드웨이, 타임스퀘어, 자유의 여신상이 있습니다.",
        "latitude": 40.7128,
        "longitude": -74.0060,
        "themes": ["couple", "family", "solo", "friends", "culture"],
        "suitable_for_children": True,
        "family_size_recommended": {"min": 1, "max": 10},
        "activities": ["culture", "theater", "shopping", "restaurant", "nightlife"],
        "images": [
            "https://via.placeholder.com/400x300?text=New+York+City",
            "https://via.placeholder.com/400x300?text=Times+Square"
        ],
        "useful_links": {
            "tourism_board": "https://www.nycgo.com",
            "official_map": "https://maps.google.com/newyork",
            "hotels": ["https://agoda.com/newyork"],
            "restaurants": ["https://www.yelp.com"]
        }
    },
    {
        "name": "바디",
        "location": "인도네시아",
        "country": "Indonesia",
        "description": "아름다운 해변, 힌두 사원, 요가 리트릿이 있는 휴양지입니다.",
        "latitude": -8.6500,
        "longitude": 115.2167,
        "themes": ["couple", "family", "relaxation", "beach", "yoga"],
        "suitable_for_children": True,
        "family_size_recommended": {"min": 2, "max": 8},
        "activities": ["beach", "yoga", "temple", "water_sports", "massage", "hiking"],
        "images": [
            "https://via.placeholder.com/400x300?text=Bali+Beach",
            "https://via.placeholder.com/400x300?text=Bali+Temple"
        ],
        "useful_links": {
            "tourism_board": "https://www.balitoursim.travel",
            "official_map": "https://maps.google.com/bali",
            "hotels": ["https://agoda.com/bali"],
            "restaurants": ["https://www.tripadvisor.com/bali"]
        }
    }
]


def seed_destinations(db: Session):
    """
    데이터베이스에 샘플 여행지 데이터 추가
    """
    # 기존 데이터 확인
    existing = db.query(Destination).first()
    if existing:
        print("✅ 이미 여행지 데이터가 존재합니다. 건너뜁니다.")
        return

    # 샘플 데이터 추가
    for dest_data in SAMPLE_DESTINATIONS:
        destination = Destination(**dest_data)
        db.add(destination)

    db.commit()
    print(f"✅ {len(SAMPLE_DESTINATIONS)}개의 여행지 데이터가 추가되었습니다!")


# 샘플 장거리 교통편 데이터
SAMPLE_LONG_DISTANCE = [
    {
        "type": "flight",
        "departure_city": "서울",
        "arrival_city": "제주",
        "departure_time": datetime.now() + timedelta(days=1, hours=8),
        "arrival_time": datetime.now() + timedelta(days=1, hours=9, minutes=30),
        "duration_minutes": 90,
        "price": 85000,
        "currency": "KRW",
        "provider": "Korean Air",
        "provider_code": "KE1201",
        "booking_methods": [
            {
                "platform": "Official Website",
                "url": "https://www.koreanair.com",
                "how_to": "Direct booking"
            }
        ],
        "directions": "서울 김포공항 → 제주 국제공항"
    },
    {
        "type": "flight",
        "departure_city": "서울",
        "arrival_city": "도쿄",
        "departure_time": datetime.now() + timedelta(days=2, hours=10),
        "arrival_time": datetime.now() + timedelta(days=2, hours=14),
        "duration_minutes": 210,
        "price": 150000,
        "currency": "KRW",
        "provider": "Asiana Airlines",
        "provider_code": "OZ101",
        "booking_methods": [
            {
                "platform": "Official Website",
                "url": "https://www.asiana.co.kr",
                "how_to": "Direct booking"
            }
        ],
        "directions": "서울 인천공항 → 나리타 국제공항"
    },
    {
        "type": "train",
        "departure_city": "서울",
        "arrival_city": "부산",
        "departure_time": datetime.now() + timedelta(days=1, hours=9),
        "arrival_time": datetime.now() + timedelta(days=1, hours=14),
        "duration_minutes": 300,
        "price": 65000,
        "currency": "KRW",
        "provider": "KTX (Korean Train Express)",
        "provider_code": "KTX110",
        "booking_methods": [
            {
                "platform": "Korail",
                "url": "https://www.letskorail.com",
                "how_to": "Online booking"
            }
        ],
        "directions": "서울역 → 부산역"
    },
    {
        "type": "bus",
        "departure_city": "서울",
        "arrival_city": "제주",
        "departure_time": datetime.now() + timedelta(days=1, hours=15),
        "arrival_time": datetime.now() + timedelta(days=2, hours=7),
        "duration_minutes": 840,
        "price": 35000,
        "currency": "KRW",
        "provider": "Jeju Express",
        "provider_code": "JX001",
        "booking_methods": [
            {
                "platform": "Express Bus",
                "url": "https://www.jejuexpress.co.kr",
                "how_to": "Online or terminal booking"
            }
        ],
        "directions": "서울 강남 버스터미널 → 제주 시외버스터미널"
    }
]

# 샘플 지역 교통편 데이터
SAMPLE_LOCAL_TRANSPORT = [
    {
        "destination_id": 1,  # 제주도
        "transport_type": "bus",
        "city": "제주",
        "route_number": "100-1",
        "route_details": ["제주시청", "신광로터리", "애월읍", "한라산"],
        "frequency": "10-15분 간격",
        "operating_hours": {"start": "06:00", "end": "23:00"},
        "fare": 2500,
        "currency": "KRW",
        "payment_methods": ["cash", "card", "app"],
        "card_types": ["T-money", "Naver Pay"],
        "useful_links": {
            "timetable": "https://jejubus.co.kr",
            "route_info": "https://map.naver.com/jeju"
        },
        "directions": "신제주 → 한라산 입구"
    },
    {
        "destination_id": 2,  # 서울
        "transport_type": "subway",
        "city": "서울",
        "route_number": "Line 2",
        "route_details": ["강남역", "교대역", "서초역", "약수역"],
        "frequency": "3-5분 간격",
        "operating_hours": {"start": "05:30", "end": "23:30"},
        "fare": 2500,
        "currency": "KRW",
        "payment_methods": ["card", "app"],
        "card_types": ["T-money", "Naver Pay", "Kakao Pay"],
        "useful_links": {
            "timetable": "https://www.seoulmetro.co.kr",
            "route_info": "https://map.naver.com/seoul"
        },
        "directions": "강남 ~ 서초"
    },
    {
        "destination_id": 2,  # 서울
        "transport_type": "taxi",
        "city": "서울",
        "base_fare": 3800,
        "distance_per_km": 1000,
        "time_unit_fare": 200,
        "calling_apps": ["KakaoT", "Naver Map", "Tmap"],
        "tip_culture": "Optional",
        "payment_methods": ["cash", "card"],
        "useful_links": {
            "app_download": "https://www.kakao.com",
            "info": "https://www.taxyseoul.co.kr"
        },
        "operating_hours": {"start": "00:00", "end": "23:59"}
    },
    {
        "destination_id": 4,  # 도쿄
        "transport_type": "subway",
        "city": "도쿄",
        "route_number": "Yamanote Line",
        "route_details": ["신주쿠역", "시부야역", "하라주쿠역", "메지로역"],
        "frequency": "2-3분 간격",
        "operating_hours": {"start": "05:00", "end": "24:00"},
        "fare": 160,
        "currency": "JPY",
        "payment_methods": ["card", "app"],
        "card_types": ["Suica", "Pasmo"],
        "useful_links": {
            "timetable": "https://www.jreast.co.jp",
            "route_info": "https://maps.google.com/tokyo"
        },
        "directions": "신주쿠 순환선"
    }
]


def seed_long_distance_transportation(db: Session):
    """
    샘플 장거리 교통편 데이터 추가
    """
    existing = db.query(LongDistanceTransportation).first()
    if existing:
        print("✅ 이미 장거리 교통편 데이터가 존재합니다. 건너뜁니다.")
        return

    for transport_data in SAMPLE_LONG_DISTANCE:
        transport = LongDistanceTransportation(**transport_data)
        db.add(transport)

    db.commit()
    print(f"✅ {len(SAMPLE_LONG_DISTANCE)}개의 장거리 교통편 데이터가 추가되었습니다!")


def seed_local_transportation(db: Session):
    """
    샘플 지역 교통편 데이터 추가
    """
    existing = db.query(LocalTransportation).first()
    if existing:
        print("✅ 이미 지역 교통편 데이터가 존재합니다. 건너뜁니다.")
        return

    for transport_data in SAMPLE_LOCAL_TRANSPORT:
        transport = LocalTransportation(**transport_data)
        db.add(transport)

    db.commit()
    print(f"✅ {len(SAMPLE_LOCAL_TRANSPORT)}개의 지역 교통편 데이터가 추가되었습니다!")


def clear_destinations(db: Session):
    """
    모든 여행지 데이터 삭제 (테스트용)
    """
    db.query(Destination).delete()
    db.commit()
    print("✅ 모든 여행지 데이터가 삭제되었습니다!")


if __name__ == "__main__":
    from app.database import SessionLocal

    db = SessionLocal()
    try:
        seed_destinations(db)
    finally:
        db.close()
