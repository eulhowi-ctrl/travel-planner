# 🧪 테스트 가이드 - Travel Planner

애플리케이션을 테스트하는 3가지 방법을 소개합니다.

---

## 레벨 1️⃣: 빠른 테스트 (2분)

서버가 정상 작동하는지 확인하는 가장 간단한 방법입니다.

### Step 1: 서버 시작
```bash
docker-compose up -d
```

### Step 2: 헬스 체크
```bash
curl http://localhost:8000/api/v1/health
```

**예상 응답:**
```json
{
  "status": "healthy",
  "api": "Travel Planner API",
  "version": "1.0.0",
  "timestamp": "2026-07-10T12:00:00"
}
```

### Step 3: API 문서 확인
브라우저에서 열기:
```
http://localhost:8000/docs
```

✅ 성공! 서버가 정상 작동 중입니다.

---

## 레벨 2️⃣: 수동 API 테스트 (20분)

curl을 사용한 기본적인 API 테스트입니다.

### 1. 사용자 등록

```bash
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "Password123!",
    "full_name": "테스트 사용자"
  }'
```

**예상 응답:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "테스트 사용자",
  "created_at": "2026-07-10T12:00:00"
}
```

### 2. 로그인

```bash
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=Password123!"
```

**예상 응답:**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

⚠️ **중요**: `access_token` 값을 복사하세요. 다음 요청들에서 사용합니다.

### 3. 현재 사용자 정보 조회

```bash
# TOKEN을 위의 access_token 값으로 바꾸세요
curl -X GET http://localhost:8000/api/v1/users/me \
  -H "Authorization: Bearer TOKEN"
```

**예상 응답:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "테스트 사용자"
}
```

### 4. 여행지 목록 조회

```bash
curl -X GET "http://localhost:8000/api/v1/destinations?skip=0&limit=10" \
  -H "Authorization: Bearer TOKEN"
```

**예상 응답:**
```json
{
  "items": [
    {
      "id": 1,
      "name": "제주도",
      "country": "South Korea",
      "location": "Jeju",
      "description": "..."
    },
    ...
  ],
  "total": 50
}
```

### 5. 여행지 검색

```bash
curl -X POST http://localhost:8000/api/v1/destinations/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "keyword": "제주",
    "skip": 0,
    "limit": 10
  }'
```

### 6. 프로필 생성

```bash
curl -X POST http://localhost:8000/api/v1/users/profile \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "travel_style": "family",
    "preferred_activities": ["hiking", "beach"],
    "budget_preference": "mid",
    "travel_pace": "relaxed"
  }'
```

### 7. 여행 계획 생성

```bash
curl -X POST http://localhost:8000/api/v1/itineraries \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "title": "제주도 가족 여행",
    "departure_city": "Seoul",
    "destination_ids": [1, 2],
    "start_date": "2026-08-01",
    "end_date": "2026-08-05",
    "theme": "family",
    "budget": 2000000,
    "description": "여름 휴가"
  }'
```

**응답에서 itinerary_id를 복사하세요** (예: 1)

### 8. 일정 자동 생성

```bash
# ITINERARY_ID를 위에서 받은 ID로 바꾸세요
curl -X POST http://localhost:8000/api/v1/itineraries/ITINERARY_ID/generate-days \
  -H "Authorization: Bearer TOKEN"
```

**예상 응답:**
```json
{
  "message": "Itinerary days generated successfully",
  "itinerary_id": 1,
  "total_days": 5
}
```

### 9. 예산 추가

```bash
curl -X POST http://localhost:8000/api/v1/budgets \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer TOKEN" \
  -d '{
    "itinerary_id": 1,
    "category": "flight",
    "item_name": "항공권",
    "estimated_cost": 400000,
    "actual_cost": 380000,
    "notes": "서울-제주 왕복"
  }'
```

### 10. 예산 요약 조회

```bash
curl -X GET http://localhost:8000/api/v1/budgets/summary/1 \
  -H "Authorization: Bearer TOKEN"
```

**예상 응답:**
```json
{
  "itinerary_id": 1,
  "total_estimated": 2000000,
  "total_actual": 1950000,
  "remaining": 50000,
  "categories": {
    "flight": {"estimated": 400000, "actual": 380000},
    "accommodation": {"estimated": 800000, "actual": 800000},
    ...
  }
}
```

### 11. 환율 변환

```bash
curl -X GET "http://localhost:8000/api/v1/budgets/convert?amount=1000000&from_currency=KRW&to_currency=USD" \
  -H "Authorization: Bearer TOKEN"
```

**예상 응답:**
```json
{
  "from_currency": "KRW",
  "to_currency": "USD",
  "amount": 1000000,
  "converted_amount": 750.00
}
```

### 12. 교통 정보 검색

```bash
curl -X GET "http://localhost:8000/api/v1/transportation/long-distance?departure_city=Seoul&arrival_city=Jeju" \
  -H "Authorization: Bearer TOKEN"
```

### 13. QR 코드 생성

```bash
# 기본 QR 코드
curl -X GET "http://localhost:8000/api/v1/qr-codes/generate?data=https://example.com&size=200&format=png" \
  -H "Authorization: Bearer TOKEN"
```

**응답:**
```json
{
  "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=..."
}
```

---

## 레벨 3️⃣: 완전한 통합 테스트 (30분)

전체 워크플로우를 자동화된 스크립트로 테스트합니다.

### 테스트 스크립트 작성

파일: `test_integration.sh`

```bash
#!/bin/bash

# 색상
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# API URL
BASE_URL="http://localhost:8000/api/v1"

# 결과 추적
PASSED=0
FAILED=0

# 테스트 함수
test_endpoint() {
    local name="$1"
    local method="$2"
    local endpoint="$3"
    local data="$4"
    local expected_code="$5"
    local token="$6"
    
    echo -n "테스트: $name ... "
    
    if [ -z "$token" ]; then
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            ${data:+-d "$data"})
    else
        response=$(curl -s -w "\n%{http_code}" -X "$method" "$BASE_URL$endpoint" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $token" \
            ${data:+-d "$data"})
    fi
    
    http_code=$(echo "$response" | tail -n1)
    body=$(echo "$response" | sed '$d')
    
    if [ "$http_code" = "$expected_code" ]; then
        echo -e "${GREEN}✓ PASS (HTTP $http_code)${NC}"
        PASSED=$((PASSED + 1))
        echo "$body"
    else
        echo -e "${RED}✗ FAIL (Expected: $expected_code, Got: $http_code)${NC}"
        FAILED=$((FAILED + 1))
        echo "$body"
    fi
    echo ""
}

echo "=========================================="
echo "Travel Planner 통합 테스트 시작"
echo "=========================================="
echo ""

# 1. 헬스 체크
test_endpoint "헬스 체크" "GET" "/health" "" "200"

# 2. 사용자 등록
echo "1️⃣  사용자 인증 테스트"
user_data='{
  "email": "test@example.com",
  "password": "TestPassword123!",
  "full_name": "테스트 사용자"
}'
response=$(curl -s -X POST "$BASE_URL/users/register" \
    -H "Content-Type: application/json" \
    -d "$user_data")
test_endpoint "회원가입" "POST" "/users/register" "$user_data" "201"
USER_ID=$(echo "$response" | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')

# 3. 로그인
login_data='username=test@example.com&password=TestPassword123!'
response=$(curl -s -X POST "$BASE_URL/auth/login" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "$login_data")
test_endpoint "로그인" "POST" "/auth/login" "$login_data" "200"
TOKEN=$(echo "$response" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)

if [ -z "$TOKEN" ]; then
    echo -e "${RED}토큰 추출 실패!${NC}"
    exit 1
fi

echo -e "${YELLOW}토큰: ${TOKEN:0:30}...${NC}"
echo ""

# 4. 프로필 조회
echo "2️⃣  프로필 테스트"
test_endpoint "프로필 조회" "GET" "/users/me" "" "200" "$TOKEN"

# 5. 프로필 생성
profile_data='{
  "travel_style": "family",
  "preferred_activities": ["hiking", "beach"],
  "budget_preference": "mid"
}'
test_endpoint "프로필 생성" "POST" "/users/profile" "$profile_data" "201" "$TOKEN"

# 6. 여행지 검색
echo "3️⃣  여행지 테스트"
test_endpoint "여행지 목록" "GET" "/destinations?skip=0&limit=10" "" "200" "$TOKEN"

search_data='{
  "keyword": "제주",
  "skip": 0,
  "limit": 10
}'
test_endpoint "여행지 검색" "POST" "/destinations/search" "$search_data" "200" "$TOKEN"

# 7. 여행 계획 생성
echo "4️⃣  여행 계획 테스트"
itinerary_data='{
  "title": "테스트 여행",
  "departure_city": "Seoul",
  "destination_ids": [1, 2],
  "start_date": "2026-08-01",
  "end_date": "2026-08-05",
  "theme": "family",
  "budget": 2000000
}'
response=$(curl -s -X POST "$BASE_URL/itineraries" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $TOKEN" \
    -d "$itinerary_data")
test_endpoint "여행 계획 생성" "POST" "/itineraries" "$itinerary_data" "201" "$TOKEN"
ITINERARY_ID=$(echo "$response" | grep -o '"id":[0-9]*' | head -1 | grep -o '[0-9]*')

if [ -z "$ITINERARY_ID" ]; then
    echo -e "${RED}여행 계획 ID 추출 실패!${NC}"
    exit 1
fi

echo -e "${YELLOW}여행 계획 ID: $ITINERARY_ID${NC}"
echo ""

# 8. 일정 자동 생성
test_endpoint "일정 생성" "POST" "/itineraries/$ITINERARY_ID/generate-days" "" "200" "$TOKEN"

# 9. 예산 테스트
echo "5️⃣  예산 테스트"
budget_data='{
  "itinerary_id": '$ITINERARY_ID',
  "category": "flight",
  "item_name": "항공권",
  "estimated_cost": 400000,
  "actual_cost": 380000
}'
test_endpoint "예산 추가" "POST" "/budgets" "$budget_data" "201" "$TOKEN"

test_endpoint "예산 요약" "GET" "/budgets/summary/$ITINERARY_ID" "" "200" "$TOKEN"

test_endpoint "예산 통계" "GET" "/budgets/stats/$ITINERARY_ID" "" "200" "$TOKEN"

# 10. 환율 변환
echo "6️⃣  환율 변환 테스트"
test_endpoint "KRW→USD 변환" "GET" "/budgets/convert?amount=1000000&from_currency=KRW&to_currency=USD" "" "200" "$TOKEN"

# 11. 교통 정보
echo "7️⃣  교통 정보 테스트"
test_endpoint "교통 검색" "GET" "/transportation/long-distance?departure_city=Seoul" "" "200" "$TOKEN"

# 12. QR 코드
echo "8️⃣  QR 코드 테스트"
test_endpoint "QR 생성" "GET" "/qr-codes/generate?data=https://example.com&size=200" "" "200" "$TOKEN"

# 결과 출력
echo "=========================================="
echo "테스트 결과"
echo "=========================================="
echo -e "${GREEN}✓ 통과: $PASSED${NC}"
echo -e "${RED}✗ 실패: $FAILED${NC}"
echo "총합: $((PASSED + FAILED))"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}모든 테스트 통과! ✨${NC}"
    exit 0
else
    echo -e "${RED}일부 테스트 실패${NC}"
    exit 1
fi
```

### 테스트 실행

```bash
# 스크립트 저장
cd /tmp/travel-planner
cat > test_integration.sh << 'SCRIPT'
[위의 bash 스크립트 내용]
SCRIPT

# 실행 권한 부여
chmod +x test_integration.sh

# 테스트 실행
./test_integration.sh
```

**예상 출력:**
```
==========================================
Travel Planner 통합 테스트 시작
==========================================

테스트: 헬스 체크 ... ✓ PASS (HTTP 200)
...

==========================================
테스트 결과
==========================================
✓ 통과: 12
✗ 실패: 0
총합: 12

모든 테스트 통과! ✨
```

---

## 레벨 4️⃣: 웹 UI 테스트 (30분)

브라우저에서 직접 사용자 인터페이스를 테스트합니다.

### 1. 로그인 테스트

1. http://localhost 접속
2. 이메일: `test@example.com`
3. 비밀번호: `TestPassword123!`
4. 로그인 버튼 클릭

**예상 결과:**
- ✅ 대시보드 페이지로 이동
- ✅ 사용자 이름 표시

### 2. 여행지 검색

1. "여행지 검색" 버튼 클릭
2. 검색 필터 사용:
   - 키워드: "제주"
   - 테마: "Beach"
   - 활동: "Hiking"
3. 검색 버튼 클릭

**예상 결과:**
- ✅ 여행지 카드 표시
- ✅ 페이지네이션 작동
- ✅ "상세" 및 "추가" 버튼 작동

### 3. 여행 계획 생성

1. "새 여행 계획" 버튼 클릭
2. **Step 1**: 기본 정보 입력
   - 제목: "테스트 여행"
   - 출발지: "Seoul"
   - 시작일: "2026-08-01"
   - 종료일: "2026-08-05"
   - 다음 버튼 클릭

3. **Step 2**: 목적지 선택
   - 여행지 2개 선택
   - 다음 버튼 클릭

4. **Step 3**: 테마 선택
   - "Family" 선택
   - 실시간 예산 계산 확인
   - 다음 버튼 클릭

5. **Step 4**: 완료
   - 성공 메시지 확인
   - 예산 페이지로 자동 이동

**예상 결과:**
- ✅ 각 단계에서 유효성 검사
- ✅ 실시간 예산 계산
- ✅ 성공 메시지 표시

### 4. 예산 관리

1. 예산 페이지에서:
   - 통계 카드 확인
   - 예산 항목 추가
     - 카테고리: "Flight"
     - 항목: "항공권"
     - 예상: "400000"
     - 실제: "380000"
   - 추가 버튼 클릭

2. 환율 변환:
   - KRW: 1000000 입력
   - USD 선택
   - 변환 결과 확인

**예상 결과:**
- ✅ 카테고리별 비용 표시
- ✅ 환율 자동 계산
- ✅ 실시간 업데이트

---

## 📊 테스트 체크리스트

### API 테스트 (14개)
- [ ] 헬스 체크
- [ ] 회원가입
- [ ] 로그인
- [ ] 프로필 조회
- [ ] 프로필 생성
- [ ] 여행지 목록
- [ ] 여행지 검색
- [ ] 여행 계획 생성
- [ ] 일정 자동 생성
- [ ] 예산 추가
- [ ] 예산 요약
- [ ] 환율 변환
- [ ] 교통 검색
- [ ] QR 코드 생성

### UI 테스트 (12개)
- [ ] 로그인 작동
- [ ] 대시보드 표시
- [ ] 여행지 검색 필터
- [ ] 여행지 페이지네이션
- [ ] 여행 계획 4단계 폼
- [ ] 실시간 예산 계산
- [ ] 예산 카테고리 표시
- [ ] 환율 변환기
- [ ] 모바일 반응형 (작은 화면)
- [ ] 태블릿 반응형 (중간 화면)
- [ ] 데스크톱 반응형 (큰 화면)
- [ ] 팁 및 조언 표시

### 데이터베이스 테스트 (8개)
- [ ] 사용자 데이터 저장
- [ ] 프로필 데이터 저장
- [ ] 여행지 샘플 데이터 로드
- [ ] 여행 계획 생성
- [ ] 일정 항목 생성
- [ ] 예산 항목 저장
- [ ] 외래키 관계 확인
- [ ] 데이터 조회 성능

---

## 🐛 문제 발생 시

### 포트 이미 사용 중
```bash
# 사용 중인 포트 확인
lsof -i :8000
lsof -i :5432

# docker-compose.yml에서 포트 변경
ports:
  - "8080:8000"
```

### API 오류
```bash
# 로그 확인
docker-compose logs -f api

# 특정 오류 검색
docker-compose logs api | grep ERROR
```

### 데이터베이스 연결 오류
```bash
# 데이터베이스 상태 확인
docker-compose ps postgres

# 데이터베이스 재시작
docker-compose restart postgres

# 완전 초기화
docker-compose down -v
docker-compose up -d
```

### Token 오류
```
"detail": "Not authenticated"
```
→ Authorization 헤더 확인
→ Token 값이 정확한지 확인
→ Token 만료 여부 확인 (30분)

---

## 📈 성능 테스트 (선택사항)

### 응답 시간 측정

```bash
# 헬스 체크 응답 시간
time curl http://localhost:8000/api/v1/health

# API 응답 시간
time curl -H "Authorization: Bearer TOKEN" \
  http://localhost:8000/api/v1/destinations?skip=0&limit=100
```

**목표:**
- 헬스 체크: < 100ms
- 일반 API: < 500ms
- 복잡한 쿼리: < 1000ms

### 동시 요청 테스트

```bash
# 10개 동시 요청
for i in {1..10}; do
  curl -s http://localhost:8000/api/v1/health &
done
wait
```

---

## 🎯 최종 체크

모든 테스트를 마친 후:

- [ ] 헬스 체크: ✓ 통과
- [ ] API 테스트: ✓ 14/14 통과
- [ ] UI 테스트: ✓ 12/12 통과
- [ ] 데이터베이스: ✓ 정상
- [ ] 문서: ✓ 최신

**준비 완료! 배포하세요. 🚀**

---

**테스트 가이드 끝**
