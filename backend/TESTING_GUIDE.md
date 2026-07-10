# 🧪 사용자 인증 API 테스트 가이드

## 📚 API 엔드포인트 목록

### 사용자 관련 API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | `/api/v1/users/register` | 회원가입 |
| POST | `/api/v1/users/login` | 로그인 |
| GET | `/api/v1/users/me` | 내 정보 조회 |
| POST | `/api/v1/users/profile` | 프로필 생성 |
| GET | `/api/v1/users/profile` | 프로필 조회 |
| PUT | `/api/v1/users/profile` | 프로필 수정 |
| PUT | `/api/v1/users/me` | 사용자 정보 수정 |
| DELETE | `/api/v1/users/me` | 계정 비활성화 |

---

## 🚀 빠른 시작

### 1단계: 서버 시작

```bash
cd backend
python -m app.main
```

### 2단계: Swagger UI에서 테스트

브라우저에서 `http://localhost:8000/docs` 접속

---

## 🧪 API 테스트 예시

### 1️⃣ 회원가입 (Register)

**요청:**
```bash
curl -X POST "http://localhost:8000/api/v1/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "john_doe",
    "password": "SecurePassword123!"
  }'
```

**성공 응답 (201):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "is_active": true,
  "created_at": "2026-07-10T12:34:56"
}
```

**에러 응답 (400):**
```json
{
  "detail": "이미 사용 중인 이메일입니다."
}
```

---

### 2️⃣ 로그인 (Login)

**요청:**
```bash
curl -X POST "http://localhost:8000/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePassword123!"
  }'
```

**성공 응답 (200):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

💡 **이 토큰을 저장했다가 다른 API 요청 시 사용합니다!**

---

### 3️⃣ 내 정보 조회 (Get Current User)

**요청:**
```bash
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

**성공 응답 (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "john_doe",
  "is_active": true,
  "created_at": "2026-07-10T12:34:56",
  "profile": {
    "id": 1,
    "user_id": 1,
    "travel_theme": "family",
    "family_size": 4,
    "has_children": true,
    "children_ages": [3, 8],
    "preferred_activities": ["hiking", "beach"],
    "budget_level": "standard"
  }
}
```

---

### 4️⃣ 프로필 생성 (Create Profile)

**요청:**
```bash
curl -X POST "http://localhost:8000/api/v1/users/profile" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "travel_theme": "family",
    "family_size": 4,
    "has_children": true,
    "children_ages": [3, 8],
    "preferred_activities": ["hiking", "beach", "museum"],
    "budget_level": "standard"
  }'
```

**성공 응답 (201):**
```json
{
  "id": 1,
  "user_id": 1,
  "travel_theme": "family",
  "family_size": 4,
  "has_children": true,
  "children_ages": [3, 8],
  "preferred_activities": ["hiking", "beach", "museum"],
  "budget_level": "standard"
}
```

---

### 5️⃣ 프로필 수정 (Update Profile)

**요청:**
```bash
curl -X PUT "http://localhost:8000/api/v1/users/profile" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "preferred_activities": ["beach", "restaurant", "shopping"],
    "budget_level": "luxury"
  }'
```

**성공 응답 (200):**
```json
{
  "id": 1,
  "user_id": 1,
  "travel_theme": "family",
  "family_size": 4,
  "has_children": true,
  "children_ages": [3, 8],
  "preferred_activities": ["beach", "restaurant", "shopping"],
  "budget_level": "luxury"
}
```

---

### 6️⃣ 사용자 정보 수정 (Update User)

**요청:**
```bash
curl -X PUT "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newemail@example.com",
    "username": "new_username",
    "password": "NewPassword456!"
  }'
```

**성공 응답 (200):**
```json
{
  "id": 1,
  "email": "newemail@example.com",
  "username": "new_username",
  "is_active": true,
  "created_at": "2026-07-10T12:34:56"
}
```

---

### 7️⃣ 계정 비활성화 (Deactivate Account)

**요청:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN_HERE"
```

**성공 응답 (204):**
- 응답 본문 없음

---

## 📱 Swagger UI에서 테스트하기

1. `http://localhost:8000/docs` 접속
2. **Authorize** 버튼 클릭
3. Bearer Token 입력 필드에 로그인 후 받은 `access_token` 입력
4. API 테스트

---

## 🔑 여행 테마 (travel_theme) 옵션

| 값 | 설명 |
|----|------|
| `couple` | 커플 여행 |
| `family` | 가족 여행 |
| `solo` | 혼자 여행 |
| `friends` | 친구 여행 |

---

## 💰 예산 수준 (budget_level) 옵션

| 값 | 설명 |
|----|------|
| `budget` | 저예산 |
| `standard` | 표준 |
| `luxury` | 럭셔리 |

---

## 📝 선호 활동 (preferred_activities) 예시

```json
[
  "hiking",           // 등산
  "beach",            // 해변
  "culture",          // 문화
  "museum",           // 박물관
  "restaurant",       // 레스토랑
  "shopping",         // 쇼핑
  "adventure",        // 모험
  "relaxation"        // 휴식
]
```

---

## ⚠️ 일반적인 에러 및 해결책

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```
**해결:** 토큰이 만료되었거나 잘못되었습니다. 다시 로그인하세요.

### 400 Bad Request
```json
{
  "detail": "이미 사용 중인 이메일입니다."
}
```
**해결:** 다른 이메일을 사용하세요.

### 422 Unprocessable Entity
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "invalid email format",
      "type": "value_error.email"
    }
  ]
}
```
**해결:** 유효한 이메일 형식을 입력하세요.

---

## 🧪 통합 테스트 시나리오

### 시나리오 1: 새 사용자 등록 및 프로필 설정

```bash
# 1. 회원가입
curl -X POST "http://localhost:8000/api/v1/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "family_travel@example.com",
    "username": "family_traveler",
    "password": "FamilyTrip2026!"
  }'

# 2. 로그인
curl -X POST "http://localhost:8000/api/v1/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "family_travel@example.com",
    "password": "FamilyTrip2026!"
  }'
# 응답에서 access_token 복사!

# 3. 프로필 생성
curl -X POST "http://localhost:8000/api/v1/users/profile" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{
    "travel_theme": "family",
    "family_size": 4,
    "has_children": true,
    "children_ages": [5, 10],
    "preferred_activities": ["beach", "theme_park", "restaurant"],
    "budget_level": "standard"
  }'

# 4. 정보 조회
curl -X GET "http://localhost:8000/api/v1/users/me" \
  -H "Authorization: Bearer <YOUR_TOKEN>"
```

---

## 📊 데이터베이스 확인

### SQLite 사용 시

```bash
# SQLite 데이터베이스 확인
sqlite3 travel_planner.db

# 사용자 테이블 조회
sqlite> SELECT * FROM users;
sqlite> SELECT * FROM user_profiles;
```

### PostgreSQL 사용 시

```bash
# PostgreSQL 연결
psql -U user -d travel_planner_db

-- 사용자 테이블 조회
SELECT * FROM users;
SELECT * FROM user_profiles;
```

---

## ✅ 테스트 체크리스트

- [ ] 회원가입 성공 (201)
- [ ] 중복 이메일 방지 (400)
- [ ] 중복 사용자명 방지 (400)
- [ ] 로그인 성공 (200, access_token 반환)
- [ ] 잘못된 비밀번호 (401)
- [ ] 토큰 없이 /me 접속 (401)
- [ ] /me에서 프로필 정보 조회 (200)
- [ ] 프로필 생성 (201)
- [ ] 프로필 수정 (200)
- [ ] 사용자 정보 수정 (200)
- [ ] 계정 비활성화 (204)
- [ ] 비활성화 계정 로그인 거부 (403)

---

## 🎉 완료!

사용자 인증 시스템이 완벽하게 작동합니다!

**다음 단계:** Task #4 - 여행지 검색 및 추천 기능 구현
