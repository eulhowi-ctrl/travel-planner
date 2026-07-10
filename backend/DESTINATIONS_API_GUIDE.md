# 🌍 여행지 검색 및 추천 API 가이드

## 📚 API 엔드포인트 목록

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/v1/destinations` | 전체 여행지 목록 |
| GET | `/api/v1/destinations/{id}` | 여행지 상세 정보 |
| POST | `/api/v1/destinations/search` | 여행지 검색 |
| GET | `/api/v1/destinations/recommend/for-me` | 맞춤형 추천 |
| GET | `/api/v1/destinations/theme/{theme}` | 테마별 조회 |
| GET | `/api/v1/destinations/filter/family-friendly` | 가족 친화적 |
| GET | `/api/v1/destinations/filter/activity/{activity}` | 활동별 조회 |
| GET | `/api/v1/destinations/popular/trending` | 인기 여행지 |
| POST | `/api/v1/destinations` | 여행지 추가 (관리자) |
| PUT | `/api/v1/destinations/{id}` | 여행지 수정 (관리자) |
| DELETE | `/api/v1/destinations/{id}` | 여행지 삭제 (관리자) |
| GET | `/api/v1/destinations/stats/count` | 통계 조회 |

---

## 🚀 API 사용 예시

### 1️⃣ 전체 여행지 목록 조회

**요청:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations?skip=0&limit=5"
```

**쿼리 파라미터:**
- `skip`: 스킵할 항목 수 (기본값: 0)
- `limit`: 반환할 항목 수 (기본값: 10, 최대: 100)

**성공 응답 (200):**
```json
[
  {
    "id": 1,
    "name": "제주도",
    "location": "대한민국",
    "country": "South Korea",
    "description": "한국의 아름다운 섬으로 해변, 산, 문화유산이 풍부합니다.",
    "latitude": 33.3688,
    "longitude": 126.5412,
    "themes": ["couple", "family", "kids-friendly", "beach"],
    "suitable_for_children": true,
    "family_size_recommended": {"min": 1, "max": 10},
    "activities": ["beach", "hiking", "water_sports", "restaurant"],
    "images": [
      "https://via.placeholder.com/400x300?text=Jeju+Beach"
    ],
    "useful_links": {
      "tourism_board": "https://www.visitjeju.net",
      "hotels": ["https://agoda.com/jeju"]
    },
    "is_active": true,
    "created_at": "2026-07-10T12:34:56"
  },
  ...
]
```

---

### 2️⃣ 여행지 상세 정보 조회

**요청:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/1"
```

**성공 응답 (200):**
```json
{
  "id": 1,
  "name": "제주도",
  "location": "대한민국",
  "country": "South Korea",
  "description": "한국의 아름다운 섬으로 해변, 산, 문화유산이 풍부합니다.",
  ...
}
```

**에러 응답 (404):**
```json
{
  "detail": "여행지를 찾을 수 없습니다."
}
```

---

### 3️⃣ 여행지 검색

**키워드로 검색:**
```bash
curl -X POST "http://localhost:8000/api/v1/destinations/search?keyword=해변&limit=10"
```

**테마로 필터링:**
```bash
curl -X POST "http://localhost:8000/api/v1/destinations/search?theme=family&limit=10"
```

**위치로 검색:**
```bash
curl -X POST "http://localhost:8000/api/v1/destinations/search?location=일본&limit=10"
```

**아이 친화적 여행지:**
```bash
curl -X POST "http://localhost:8000/api/v1/destinations/search?suitable_for_children=true&limit=10"
```

**활동별 검색:**
```bash
curl -X POST "http://localhost:8000/api/v1/destinations/search?activity=beach&limit=10"
```

**복합 검색:**
```bash
curl -X POST "http://localhost:8000/api/v1/destinations/search?keyword=제주&theme=family&suitable_for_children=true&limit=5"
```

---

### 4️⃣ 맞춤형 추천 (로그인 필수)

**요청:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/recommend/for-me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

**로직:**
1. 사용자 프로필의 여행 테마로 필터링
2. 아이가 있으면 아이 친화적 여행지 우선
3. 선호 활동과 매칭되는 여행지 추천

**성공 응답 (200):**
```json
[
  {
    "id": 1,
    "name": "제주도",
    ...
  },
  {
    "id": 3,
    "name": "부산",
    ...
  }
]
```

---

### 5️⃣ 테마별 여행지 조회

**커플 여행:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/theme/couple"
```

**가족 여행:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/theme/family"
```

**혼자 여행:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/theme/solo"
```

**친구 여행:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/theme/friends"
```

---

### 6️⃣ 가족 친화적 여행지

**요청:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/filter/family-friendly?family_size=4&has_kids=true"
```

**쿼리 파라미터:**
- `family_size`: 가족 인원수 (1-10)
- `has_kids`: 아이 동반 여부 (true/false)

---

### 7️⃣ 활동별 여행지 조회

**해변:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/filter/activity/beach"
```

**등산:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/filter/activity/hiking"
```

**문화:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/filter/activity/culture"
```

**박물관:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/filter/activity/museum"
```

**음식:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/filter/activity/food"
```

**가능한 활동 종류:**
- beach (해변)
- hiking (등산)
- culture (문화)
- museum (박물관)
- restaurant (레스토랑)
- shopping (쇼핑)
- temple (사원/신사)
- theme_park (테마파크)
- water_sports (수상스포츠)
- nightlife (야생활)
- market (시장)
- yoga (요가)
- massage (마사지)
- technology (기술)
- anime (애니메)
- romantic (로맨틱)
- adventure (모험)
- relaxation (휴식)

---

### 8️⃣ 인기 여행지 (최신순)

**요청:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/popular/trending?limit=10"
```

---

### 9️⃣ 통계 조회

**요청:**
```bash
curl -X GET "http://localhost:8000/api/v1/destinations/stats/count"
```

**응답:**
```json
{
  "total": 10,
  "by_theme": {
    "couple": 8,
    "family": 9,
    "solo": 7,
    "friends": 6
  },
  "kids_friendly": 9
}
```

---

## 📱 Swagger UI에서 테스트

1. `http://localhost:8000/docs` 접속
2. **Authorize** 버튼으로 토큰 등록 (맞춤형 추천 필요)
3. 각 엔드포인트의 **Try it out** 버튼으로 테스트

---

## 🎯 여행지 테마 옵션

| 테마 | 설명 | 예시 |
|------|------|------|
| `couple` | 커플 여행 | 파리, 산토리니, 발리 |
| `family` | 가족 여행 | 제주, 싱가포르, 도쿄 |
| `solo` | 혼자 여행 | 태국, 뉴욕, 바르셀로나 |
| `friends` | 친구 여행 | 서울, 부산, 방콕 |

---

## 🎨 활동 아이콘 매핑

```json
{
  "beach": "🏖️",
  "hiking": "⛰️",
  "culture": "🏛️",
  "museum": "🖼️",
  "restaurant": "🍴",
  "shopping": "🛍️",
  "temple": "⛪",
  "theme_park": "🎢",
  "water_sports": "🏄",
  "nightlife": "🌙",
  "market": "🏪",
  "yoga": "🧘",
  "massage": "💆",
  "technology": "🤖",
  "anime": "🎌",
  "romantic": "💕",
  "adventure": "🗺️",
  "relaxation": "😌"
}
```

---

## 🧪 통합 테스트 시나리오

### 시나리오 1: 가족 여행자의 일정

```bash
# 1. 로그인하여 토큰 획득
TOKEN="your_token_here"

# 2. 가족 프로필 생성
curl -X POST "http://localhost:8000/api/v1/users/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "travel_theme": "family",
    "family_size": 4,
    "has_children": true,
    "children_ages": [3, 8],
    "preferred_activities": ["beach", "theme_park", "restaurant"],
    "budget_level": "standard"
  }'

# 3. 맞춤형 추천 받기
curl -X GET "http://localhost:8000/api/v1/destinations/recommend/for-me" \
  -H "Authorization: Bearer $TOKEN"

# 4. 아이 친화적 여행지 검색
curl -X POST "http://localhost:8000/api/v1/destinations/search?suitable_for_children=true&theme=family"

# 5. 테마파크가 있는 여행지 검색
curl -X POST "http://localhost:8000/api/v1/destinations/search?activity=theme_park"
```

### 시나리오 2: 커플 여행자의 일정

```bash
# 1. 커플 프로필 생성
curl -X POST "http://localhost:8000/api/v1/users/profile" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "travel_theme": "couple",
    "family_size": 2,
    "has_children": false,
    "preferred_activities": ["romantic", "culture", "restaurant"],
    "budget_level": "luxury"
  }'

# 2. 맞춤형 추천 받기
curl -X GET "http://localhost:8000/api/v1/destinations/recommend/for-me" \
  -H "Authorization: Bearer $TOKEN"

# 3. 로맨틱한 여행지 검색
curl -X POST "http://localhost:8000/api/v1/destinations/search?activity=romantic"
```

---

## ✅ 테스트 체크리스트

- [ ] 전체 여행지 목록 조회 (200)
- [ ] 여행지 상세 정보 조회 (200)
- [ ] 존재하지 않는 여행지 조회 (404)
- [ ] 키워드 검색 (200)
- [ ] 테마별 필터링 (200)
- [ ] 활동별 필터링 (200)
- [ ] 맞춤형 추천 (로그인 필수, 200)
- [ ] 페이지네이션 작동 여부
- [ ] 통계 조회 (200)

---

## 🎉 샘플 데이터

서버 시작 시 자동으로 10개 국가의 22개 여행지가 추가됩니다:

- 🇰🇷 **대한민국**: 제주도, 서울, 부산
- 🇯🇵 **일본**: 도쿄, 오사카
- 🇹🇭 **태국**: 방콕
- 🇸🇬 **싱가포르**: 싱가포르
- 🇫🇷 **프랑스**: 파리
- 🇺🇸 **미국**: 뉴욕
- 🇮🇩 **인도네시아**: 발리

---

## 🔄 다음 단계

- Task #5: 여행 일정 자동 생성 API
- Task #6: 예산 계산 API
- Task #7: 교통편 정보 API
- Task #8: 프론트엔드 통합

**축하합니다! 여행지 검색 및 추천 시스템이 완성되었습니다!** 🌍✈️
