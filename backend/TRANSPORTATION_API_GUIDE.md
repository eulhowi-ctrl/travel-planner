# 🚗 교통편 정보 및 예약 API 가이드

## 📚 API 엔드포인트 목록

### 장거리 교통편 (Long-Distance Transportation)

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/v1/transportation/long-distance` | 전체 장거리 교통편 목록 |
| GET | `/api/v1/transportation/long-distance/{id}` | 장거리 교통편 상세 정보 |
| POST | `/api/v1/transportation/long-distance/search` | 장거리 교통편 검색 |
| POST | `/api/v1/transportation/long-distance` | 교통편 추가 (관리자) |
| PUT | `/api/v1/transportation/long-distance/{id}` | 교통편 수정 (관리자) |
| DELETE | `/api/v1/transportation/long-distance/{id}` | 교통편 삭제 (관리자) |

### 지역 교통편 (Local Transportation)

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/v1/transportation/local` | 지역 교통편 목록 |
| GET | `/api/v1/transportation/local/{id}` | 지역 교통편 상세 정보 |
| POST | `/api/v1/transportation/local/search` | 지역 교통편 검색 |
| POST | `/api/v1/transportation/local` | 교통편 추가 (관리자) |
| PUT | `/api/v1/transportation/local/{id}` | 교통편 수정 (관리자) |
| DELETE | `/api/v1/transportation/local/{id}` | 교통편 삭제 (관리자) |

### 통계 및 정보

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/v1/transportation/stats/routes` | 교통편 통계 |
| GET | `/api/v1/transportation/tips` | 교통편 이용 팁 |

---

## 🚀 API 사용 예시

### 1️⃣ 장거리 교통편 목록 조회

**요청:**
```bash
curl -X GET "http://localhost:8000/api/v1/transportation/long-distance?skip=0&limit=10"
```

**쿼리 파라미터:**
- `skip`: 스킵할 항목 수 (기본값: 0)
- `limit`: 반환할 항목 수 (기본값: 10, 최대: 100)

**성공 응답 (200):**
```json
[
  {
    "id": 1,
    "type": "flight",
    "departure_city": "서울",
    "arrival_city": "제주",
    "departure_time": "2026-07-11T08:00:00",
    "arrival_time": "2026-07-11T09:30:00",
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
    "directions": "서울 김포공항 → 제주 국제공항",
    "created_at": "2026-07-10T12:34:56"
  }
]
```

---

### 2️⃣ 장거리 교통편 검색

**요청:**
```bash
# 출발지와 도착지로 검색
curl -X POST "http://localhost:8000/api/v1/transportation/long-distance/search?departure_city=서울&arrival_city=제주"

# 교통 수단으로 검색
curl -X POST "http://localhost:8000/api/v1/transportation/long-distance/search?transport_type=flight&limit=5"

# 가격 범위로 검색
curl -X POST "http://localhost:8000/api/v1/transportation/long-distance/search?departure_city=서울&arrival_city=제주&min_price=50000&max_price=150000"
```

**쿼리 파라미터:**
- `departure_city`: 출발 도시 (예: "서울")
- `arrival_city`: 도착 도시 (예: "제주")
- `transport_type`: 교통 수단 (flight/train/bus/ferry)
- `min_price`: 최소 가격
- `max_price`: 최대 가격
- `limit`: 결과 개수 (기본값: 10)

**성공 응답 (200):**
```json
[
  {
    "id": 1,
    "type": "flight",
    "departure_city": "서울",
    "arrival_city": "제주",
    "departure_time": "2026-07-11T08:00:00",
    "arrival_time": "2026-07-11T09:30:00",
    "duration_minutes": 90,
    "price": 85000,
    "currency": "KRW",
    "provider": "Korean Air",
    "provider_code": "KE1201",
    "booking_methods": [...],
    "directions": "서울 김포공항 → 제주 국제공항",
    "created_at": "2026-07-10T12:34:56"
  }
]
```

---

### 3️⃣ 장거리 교통편 상세 정보 조회

**요청:**
```bash
curl -X GET "http://localhost:8000/api/v1/transportation/long-distance/1"
```

**성공 응답 (200):**
```json
{
  "id": 1,
  "type": "flight",
  "departure_city": "서울",
  "arrival_city": "제주",
  "departure_time": "2026-07-11T08:00:00",
  "arrival_time": "2026-07-11T09:30:00",
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
  "directions": "서울 김포공항 → 제주 국제공항",
  "created_at": "2026-07-10T12:34:56"
}
```

---

### 4️⃣ 지역 교통편 목록 조회

**요청:**
```bash
# 여행지별로 조회
curl -X GET "http://localhost:8000/api/v1/transportation/local?destination_id=1"

# 도시별로 조회
curl -X GET "http://localhost:8000/api/v1/transportation/local?city=제주"

# 교통 수단별로 조회
curl -X GET "http://localhost:8000/api/v1/transportation/local?transport_type=bus"
```

**쿼리 파라미터:**
- `destination_id`: 여행지 ID
- `city`: 도시명
- `transport_type`: 교통 수단 (bus/subway/taxi/bike/tram)
- `skip`: 스킵할 항목 수
- `limit`: 반환할 항목 수

**성공 응답 (200):**
```json
[
  {
    "id": 1,
    "destination_id": 1,
    "transport_type": "bus",
    "city": "제주",
    "route_number": "100-1",
    "route_details": ["제주시청", "신광로터리", "애월읍", "한라산"],
    "frequency": "10-15분 간격",
    "operating_hours": {
      "start": "06:00",
      "end": "23:00"
    },
    "fare": 2500,
    "currency": "KRW",
    "payment_methods": ["cash", "card", "app"],
    "card_types": ["T-money", "Naver Pay"],
    "useful_links": {
      "timetable": "https://jejubus.co.kr",
      "route_info": "https://map.naver.com/jeju"
    },
    "directions": "신제주 → 한라산 입구"
  }
]
```

---

### 5️⃣ 지역 교통편 검색

**요청:**
```bash
# 도시와 교통 수단으로 검색
curl -X POST "http://localhost:8000/api/v1/transportation/local/search?city=제주&transport_type=bus"

# 최대 요금으로 검색
curl -X POST "http://localhost:8000/api/v1/transportation/local/search?city=서울&max_fare=5000"
```

**쿼리 파라미터:**
- `city`: 도시명
- `destination_id`: 여행지 ID
- `transport_type`: 교통 수단
- `max_fare`: 최대 요금
- `limit`: 결과 개수

---

### 6️⃣ 교통편 추가 (관리자)

**장거리 교통편 추가:**
```bash
curl -X POST "http://localhost:8000/api/v1/transportation/long-distance" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "flight",
    "departure_city": "서울",
    "arrival_city": "제주",
    "departure_time": "2026-07-15T14:00:00",
    "arrival_time": "2026-07-15T15:30:00",
    "price": 85000,
    "currency": "KRW",
    "provider": "Korean Air",
    "duration_minutes": 90,
    "provider_code": "KE1234",
    "booking_methods": [
      {
        "platform": "Official Website",
        "url": "https://www.koreanair.com",
        "how_to": "Direct booking"
      }
    ],
    "directions": "서울 김포공항 → 제주 국제공항"
  }'
```

**지역 교통편 추가:**
```bash
curl -X POST "http://localhost:8000/api/v1/transportation/local" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "destination_id": 1,
    "transport_type": "bus",
    "city": "제주",
    "route_number": "100-1",
    "route_details": ["제주시청", "신광로터리"],
    "frequency": "10-15분 간격",
    "operating_hours": {
      "start": "06:00",
      "end": "23:00"
    },
    "fare": 2500,
    "currency": "KRW",
    "payment_methods": ["cash", "card"],
    "card_types": ["T-money", "Naver Pay"],
    "useful_links": {
      "timetable": "https://jejubus.co.kr"
    }
  }'
```

---

### 7️⃣ 교통편 통계 조회

**요청:**
```bash
curl -X GET "http://localhost:8000/api/v1/transportation/stats/routes"
```

**성공 응답 (200):**
```json
{
  "total_long_distance": 4,
  "total_local_transports": 4,
  "total_cities_covered": 4,
  "routes_by_type": {
    "flight": 2,
    "train": 1,
    "bus": 1
  }
}
```

---

### 8️⃣ 교통편 이용 팁 조회

**요청:**
```bash
curl -X GET "http://localhost:8000/api/v1/transportation/tips"
```

**성공 응답 (200):**
```json
{
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
```

---

## 🚗 교통 수단 종류

### 장거리 교통편 (Long-Distance)
- **flight** (항공편): 빠르지만 비쌈
- **train** (기차): 편안하고 경치 좋음
- **bus** (버스): 저렴하지만 시간이 오래 걸림
- **ferry** (페리): 섬 이동 시 사용

### 지역 교통편 (Local)
- **bus** (버스): 가장 일반적인 대중교통
- **subway** (지하철): 빠르고 시간 정확
- **taxi** (택시): 편리하지만 비쌈
- **bike** (자전거): 환경 친화적
- **tram** (트램): 일부 도시에서만 운영

---

## 📱 Swagger UI에서 테스트

1. `http://localhost:8000/docs` 접속
2. **Authorize** 버튼으로 토큰 등록 (추가/수정/삭제 필요)
3. 각 엔드포인트의 **Try it out** 버튼으로 테스트

---

## 🎯 통합 테스트 시나리오

### 시나리오 1: 제주 여행 교통편 찾기

```bash
# 1. 서울에서 제주로 가는 항공편 검색
curl -X POST "http://localhost:8000/api/v1/transportation/long-distance/search?departure_city=서울&arrival_city=제주&transport_type=flight"

# 2. 제주 지역 버스 정보 조회
curl -X GET "http://localhost:8000/api/v1/transportation/local?city=제주&transport_type=bus"

# 3. 제주 택시 정보 조회
curl -X GET "http://localhost:8000/api/v1/transportation/local?city=제주&transport_type=taxi"

# 4. 교통편 팁 확인
curl -X GET "http://localhost:8000/api/v1/transportation/tips"
```

### 시나리오 2: 도쿄 여행 교통편 찾기

```bash
# 1. 서울에서 도쿄로 가는 항공편 검색
curl -X POST "http://localhost:8000/api/v1/transportation/long-distance/search?departure_city=서울&arrival_city=도쿄"

# 2. 도쿄 지하철 정보 조회
curl -X GET "http://localhost:8000/api/v1/transportation/local?city=도쿄&transport_type=subway"

# 3. 통계 확인
curl -X GET "http://localhost:8000/api/v1/transportation/stats/routes"
```

---

## ✅ 테스트 체크리스트

- [ ] 장거리 교통편 목록 조회 (200)
- [ ] 장거리 교통편 상세 정보 조회 (200)
- [ ] 장거리 교통편 검색 - 출발/도착지 (200)
- [ ] 장거리 교통편 검색 - 교통 수단 (200)
- [ ] 장거리 교통편 검색 - 가격 범위 (200)
- [ ] 지역 교통편 목록 조회 (200)
- [ ] 지역 교통편 상세 정보 조회 (200)
- [ ] 지역 교통편 검색 - 도시별 (200)
- [ ] 지역 교통편 검색 - 교통수단별 (200)
- [ ] 교통편 추가 (로그인 필수, 201)
- [ ] 교통편 수정 (로그인 필수, 200)
- [ ] 교통편 삭제 (로그인 필수, 204)
- [ ] 통계 조회 (200)
- [ ] 팁 조회 (200)

---

## 🎉 샘플 데이터

서버 시작 시 자동으로 다음 교통편이 추가됩니다:

**장거리 교통편:**
- ✈️ 서울 → 제주 (항공편)
- ✈️ 서울 → 도쿄 (항공편)
- 🚄 서울 → 부산 (기차)
- 🚌 서울 → 제주 (버스)

**지역 교통편:**
- 🚌 제주 버스 (100-1 노선)
- 🚇 서울 지하철 (2호선)
- 🚕 서울 택시
- 🚇 도쿄 지하철 (야마노테선)

---

## 🔄 다음 단계

- Task #8: QR 코드 생성 및 통합
- Task #9: 프론트엔드 페이지 완성
- Task #10: 전체 시스템 통합 테스트

**축하합니다! 교통편 정보 API가 완성되었습니다!** 🚗✈️🚄
