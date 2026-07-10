# 🧪 통합 테스트 가이드

## 📋 테스트 환경 설정

### 1️⃣ 필수 패키지 설치

```bash
pip install fastapi uvicorn sqlalchemy python-dotenv python-multipart pydantic PyJWT passlib bcrypt
```

### 2️⃣ 서버 시작

```bash
cd backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

**예상 출력:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     ✅ 10개의 여행지 데이터가 추가되었습니다!
INFO:     ✅ 4개의 장거리 교통편 데이터가 추가되었습니다!
INFO:     ✅ 4개의 지역 교통편 데이터가 추가되었습니다!
```

### 3️⃣ API 문서 확인

브라우저에서 열기:
```
http://localhost:8000/docs
```

---

## 🧑‍💻 전체 워크플로우 테스트

### 🎬 시나리오: 제주도 가족 여행 계획하기

#### **Step 1: 사용자 등록**

```bash
curl -X POST "http://localhost:8000/api/v1/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "family@example.com",
    "username": "김가족",
    "password": "secure123!"
  }'
```

**예상 응답 (201):**
```json
{
  "id": 1,
  "email": "family@example.com",
  "username": "김가족",
  "is_active": true
}
```

**테스트 항목:**
- ✅ 사용자 생성 성공
- ✅ 중복 이메일 거부
- ✅ 비밀번호 해싱

---

#### **Step 2: 로그인**

```bash
curl -X POST "http://localhost:8000/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "family@example.com",
    "password": "secure123!"
  }'
```

**예상 응답 (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

**테스트 항목:**
- ✅ 유효한 자격증명으로 토큰 생성
- ✅ 잘못된 비밀번호 거부
- ✅ 존재하지 않는 사용자 거부

```bash
# 토큰 저장 (이후 요청에서 사용)
TOKEN="your_access_token_here"
```

---

#### **Step 3: 사용자 프로필 생성**

```bash
curl -X POST "http://localhost:8000/api/v1/users/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "travel_theme": "family",
    "family_size": 4,
    "has_children": true,
    "children_ages": [5, 8],
    "preferred_activities": ["beach", "theme_park", "restaurant"],
    "budget_level": "standard"
  }'
```

**테스트 항목:**
- ✅ 프로필 생성 성공
- ✅ 인증 필요 확인
- ✅ 유효하지 않은 데이터 거부

---

#### **Step 4: 여행지 검색**

```bash
# 전체 여행지 조회
curl -X GET "http://localhost:8000/api/v1/destinations?skip=0&limit=10"

# 테마별 검색
curl -X GET "http://localhost:8000/api/v1/destinations/theme/family"

# 조건부 검색
curl -X POST "http://localhost:8000/api/v1/destinations/search?activity=beach&suitable_for_children=true" \
  -H "Content-Type: application/json"
```

**테스트 항목:**
- ✅ 목록 조회 성공
- ✅ 필터링 작동
- ✅ 페이지네이션
- ✅ 정렬 기능

---

#### **Step 5: 맞춤형 추천**

```bash
curl -X GET "http://localhost:8000/api/v1/destinations/recommend/for-me" \
  -H "Authorization: Bearer $TOKEN"
```

**예상 응답:**
- 가족 여행 테마에 맞는 여행지
- 아이 친화적 여행지 우선
- 선호 활동과 매칭된 여행지

**테스트 항목:**
- ✅ 사용자 프로필 기반 추천
- ✅ 적절한 여행지 필터링
- ✅ 인증 필요

---

#### **Step 6: 여행 계획 생성**

```bash
curl -X POST "http://localhost:8000/api/v1/itineraries" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "2026년 여름 가족 여행",
    "departure_city": "서울",
    "start_date": "2026-08-01",
    "end_date": "2026-08-04",
    "travel_theme": "family",
    "description": "아이들과 함께하는 제주도 여행",
    "budget_allocated": 5000000
  }'
```

**예상 응답 (201):**
```json
{
  "id": 1,
  "title": "2026년 여름 가족 여행",
  "user_id": 1,
  "start_date": "2026-08-01",
  "end_date": "2026-08-04",
  "travel_theme": "family",
  "budget_allocated": 5000000,
  "is_active": true
}
```

**테스트 항목:**
- ✅ 일정 생성 성공
- ✅ 날짜 검증 (종료 > 시작)
- ✅ 사용자 소유권 확인

```bash
# 생성된 itinerary ID 저장
ITINERARY_ID=1
```

---

#### **Step 7: 일정 자동 생성**

```bash
curl -X POST "http://localhost:8000/api/v1/itineraries/$ITINERARY_ID/generate-days?destination_ids=1,2" \
  -H "Authorization: Bearer $TOKEN"
```

**예상 응답:**
```json
{
  "message": "2개의 일정이 생성되었습니다.",
  "total_days": 2,
  "itinerary_id": 1
}
```

**테스트 항목:**
- ✅ 여행일정 자동 생성
- ✅ 활동 추천 생성
- ✅ 시간대별 일정 분배

---

#### **Step 8: 예산 항목 추가**

```bash
# 항공편
curl -X POST "http://localhost:8000/api/v1/itineraries/$ITINERARY_ID/budgets" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "flight",
    "item_name": "인천-제주 왕복 항공권",
    "estimated_cost": 340000,
    "currency": "KRW",
    "notes": "4명 × 85,000원"
  }'

# 숙박비
curl -X POST "http://localhost:8000/api/v1/itineraries/$ITINERARY_ID/budgets" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "accommodation",
    "item_name": "제주 호텔 3박",
    "estimated_cost": 900000,
    "actual_cost": 850000,
    "currency": "KRW"
  }'

# 식사비
curl -X POST "http://localhost:8000/api/v1/itineraries/$ITINERARY_ID/budgets" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "category": "meal",
    "item_name": "일일 식사비",
    "estimated_cost": 600000,
    "currency": "KRW",
    "notes": "4인 × 3일"
  }'
```

**테스트 항목:**
- ✅ 항목 추가 성공
- ✅ 카테고리별 분류
- ✅ 통화 저장
- ✅ 실제 비용 입력 가능

---

#### **Step 9: 예산 조회**

```bash
# 전체 예산 항목
curl -X GET "http://localhost:8000/api/v1/itineraries/$ITINERARY_ID/budgets" \
  -H "Authorization: Bearer $TOKEN"

# 카테고리별 필터
curl -X GET "http://localhost:8000/api/v1/itineraries/$ITINERARY_ID/budgets?category=flight" \
  -H "Authorization: Bearer $TOKEN"

# 예산 요약
curl -X GET "http://localhost:8000/api/v1/itineraries/$ITINERARY_ID/budget-summary" \
  -H "Authorization: Bearer $TOKEN"
```

**예상 응답:**
```json
{
  "total_estimated": 1840000,
  "total_actual": 850000,
  "remaining_budget": 4150000,
  "by_category": {
    "flight": {
      "estimated": 340000,
      "actual": 0,
      "count": 1
    },
    "accommodation": {
      "estimated": 900000,
      "actual": 850000,
      "count": 1
    }
  }
}
```

**테스트 항목:**
- ✅ 항목 목록 조회
- ✅ 필터링 작동
- ✅ 합계 계산 정확성
- ✅ 카테고리별 분석

---

#### **Step 10: 교통편 조회**

```bash
# 장거리 교통편 검색
curl -X POST "http://localhost:8000/api/v1/transportation/long-distance/search?departure_city=서울&arrival_city=제주&transport_type=flight"

# 지역 교통편 조회
curl -X GET "http://localhost:8000/api/v1/transportation/local?city=제주&transport_type=bus"
```

**테스트 항목:**
- ✅ 교통편 검색 성공
- ✅ 필터링 작동
- ✅ 가격 정렬

---

#### **Step 11: QR 코드 생성**

```bash
# 기본 QR 코드
curl -X GET "http://localhost:8000/api/v1/qr-codes/generate?data=https://www.koreanair.com&size=200"

# 예약 QR 코드
curl -X POST "http://localhost:8000/api/v1/qr-codes/booking" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_methods": [
      {
        "platform": "Official Website",
        "url": "https://www.koreanair.com"
      }
    ]
  }'

# WiFi QR 코드
curl -X GET "http://localhost:8000/api/v1/qr-codes/wifi?ssid=Hotel-WiFi&password=password123"
```

**테스트 항목:**
- ✅ QR 코드 URL 생성
- ✅ 여러 포맷 지원
- ✅ WiFi/연락처 QR 코드

---

#### **Step 12: 통화 변환**

```bash
curl -X GET "http://localhost:8000/api/v1/budgets/currency-convert?amount=100000&from_currency=KRW&to_currency=USD"
```

**예상 응답:**
```json
{
  "original_amount": 100000,
  "from_currency": "KRW",
  "converted_amount": 77.0,
  "to_currency": "USD",
  "exchange_rate": 0.00077
}
```

**테스트 항목:**
- ✅ 환율 계산
- ✅ 여러 통화 지원
- ✅ 반올림 정확성

---

## 🔴 에러 케이스 테스트

### 1️⃣ 인증 오류

```bash
# 토큰 없이 보호된 엔드포인트 접근
curl -X GET "http://localhost:8000/api/v1/users/me"
# 예상: 403 Forbidden 또는 401 Unauthorized

# 잘못된 토큰
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer invalid_token"
# 예상: 401 Unauthorized
```

**테스트 항목:**
- ✅ 토큰 필수 확인
- ✅ 토큰 유효성 검증
- ✅ 만료된 토큰 거부

---

### 2️⃣ 소유권 확인

```bash
# 다른 사용자의 일정 접근 시도
FAKE_ITINERARY_ID=999
curl -X GET "http://localhost:8000/api/v1/itineraries/$FAKE_ITINERARY_ID" \
  -H "Authorization: Bearer $TOKEN"
# 예상: 404 Not Found
```

**테스트 항목:**
- ✅ 소유권 검증
- ✅ 무단 접근 방지
- ✅ 적절한 오류 메시지

---

### 3️⃣ 유효성 검사

```bash
# 날짜 순서 오류
curl -X POST "http://localhost:8000/api/v1/itineraries" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test",
    "departure_city": "서울",
    "start_date": "2026-08-04",
    "end_date": "2026-08-01",
    "travel_theme": "family"
  }'
# 예상: 400 Bad Request
```

**테스트 항목:**
- ✅ 날짜 검증
- ✅ 필수 필드 확인
- ✅ 데이터 형식 검증

---

## ✅ 테스트 체크리스트

### 인증 (8개)
- [ ] 사용자 등록 성공
- [ ] 중복 이메일 거부
- [ ] 로그인 성공
- [ ] 잘못된 비밀번호 거부
- [ ] 토큰 생성
- [ ] 토큰 검증
- [ ] 로그아웃
- [ ] 계정 삭제

### 여행지 (13개)
- [ ] 목록 조회
- [ ] 상세 정보 조회
- [ ] 키워드 검색
- [ ] 테마별 필터
- [ ] 활동별 필터
- [ ] 아이 친화성 필터
- [ ] 맞춤형 추천
- [ ] 가족 친화적 여행지
- [ ] 인기순 정렬
- [ ] 페이지네이션
- [ ] 통계 조회
- [ ] 여행지 추가 (관리자)
- [ ] 여행지 수정 (관리자)

### 일정 (10개)
- [ ] 일정 생성
- [ ] 일정 조회
- [ ] 일정 목록
- [ ] 자동 일정 생성
- [ ] 일정 수정
- [ ] 일정 삭제
- [ ] 활동 추가
- [ ] 활동 조회
- [ ] 예산 추정
- [ ] 통계 조회

### 예산 (9개)
- [ ] 항목 추가
- [ ] 항목 조회
- [ ] 항목 목록
- [ ] 항목 수정
- [ ] 항목 삭제
- [ ] 카테고리별 필터
- [ ] 예산 요약
- [ ] 통계 조회
- [ ] 통화 변환

### 교통편 (14개)
- [ ] 장거리 목록
- [ ] 장거리 상세
- [ ] 장거리 검색
- [ ] 장거리 추가 (관리자)
- [ ] 장거리 수정 (관리자)
- [ ] 장거리 삭제 (관리자)
- [ ] 지역 목록
- [ ] 지역 상세
- [ ] 지역 검색
- [ ] 지역 추가 (관리자)
- [ ] 지역 수정 (관리자)
- [ ] 지역 삭제 (관리자)
- [ ] 통계 조회
- [ ] 팁 조회

### QR 코드 (9개)
- [ ] 기본 QR 생성
- [ ] 예약 QR 생성
- [ ] 교통편 QR 생성
- [ ] 여행지 QR 생성
- [ ] 앱 다운로드 QR
- [ ] WiFi QR 생성
- [ ] 연락처 QR 생성
- [ ] 포맷 정보
- [ ] API 정보

---

## 📊 테스트 결과 기록

### 테스트 날짜: ___________
### 총 엔드포인트: 63개
### 통과: ___/63
### 실패: ___/63
### 성공률: ____%

### 주요 이슈:

1. 
2. 
3. 

### 개선 사항:

1. 
2. 
3. 

---

## 🎉 최종 검증 항목

- [ ] 모든 API 응답이 문서와 일치
- [ ] 에러 처리가 일관성 있음
- [ ] 인증/인가 제대로 작동
- [ ] 데이터 유효성 검사
- [ ] 성능 요구사항 충족
- [ ] 보안 정책 준수
- [ ] 프론트엔드와 백엔드 통신
- [ ] 모든 페이지 기능 확인

**축하합니다! 전체 시스템 테스트가 완료되었습니다!** 🎊
