# 📦 Travel Planner - 전체 파일 구조

## 🎯 VS Code에서 프로젝트 구성하는 방법

### 1단계: 디렉토리 생성
```bash
# 프로젝트 메인 디렉토리 생성
mkdir travel-planner
cd travel-planner

# 서브 디렉토리 생성
mkdir -p backend/app/routers backend/app/utils frontend static/qr_codes
```

### 2단계: 각 파일을 아래 경로에 생성

---

## 📂 파일 목록 및 내용

### 🔧 백엔드 설정 파일

#### `backend/requirements.txt`
- FastAPI 및 필요한 모든 라이브러리 정의
- Uvicorn, SQLAlchemy, PostgreSQL 드라이버 등

#### `backend/.env.example`
- 환경 변수 템플릿
- DATABASE_URL, SECRET_KEY, JWT 설정 등

#### `backend/.env` (생성 필요)
```
DATABASE_URL=postgresql://user:password@localhost:5432/travel_planner_db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
HOST=0.0.0.0
PORT=8000
```

---

### 🐍 백엔드 Python 파일

#### `backend/app/__init__.py`
- 패키지 초기화
- 버전 및 기본 import

#### `backend/app/main.py`
- FastAPI 애플리케이션 진입점
- CORS 설정, 정적 파일 마운트
- 헬스 체크 엔드포인트
- 라우터 include (구현 예정)

#### `backend/app/models.py` (가장 중요!)
- SQLAlchemy ORM 모델 9개 정의:
  - User, UserProfile
  - Destination
  - LongDistanceTransportation, LocalTransportation
  - Itinerary, ItineraryDay
  - Budget, QRCode

#### `backend/app/schemas.py`
- Pydantic 데이터 검증 스키마
- 모든 API 요청/응답에 대한 스키마
- Enum 정의 (TravelTheme, TransportType 등)

#### `backend/app/database.py`
- SQLAlchemy 엔진 설정
- SessionLocal 팩토리
- get_db() 의존성 함수

#### `backend/app/auth.py`
- JWT 토큰 생성/검증
- 비밀번호 해싱 (bcrypt)
- 인증 의존성 함수

#### `backend/app/utils/qr_generator.py`
- QR 코드 생성 함수
- 일괄 생성 함수
- 테스트 코드 포함

---

### 🌐 프론트엔드 파일

#### `frontend/index.html` (완성!)
- 반응형 홈페이지
- Navigation, Hero Section
- Features (6개)
- How It Works (5단계)
- Call to Action
- Login/Register Modal
- Footer

#### `frontend/style.css` (완성!)
- 전체 스타일 (약 500줄)
- 반응형 디자인
- 버튼, 모달, 카드 스타일
- 색상 변수 (CSS Custom Properties)
- 애니메이션

#### `frontend/script.js` (완성!)
- API 함수 (login, register 등)
- 모달 함수
- QR 코드 관련 함수
- 유틸리티 함수 (날짜, 통화 포맷팅 등)
- 전역 함수 export

#### `frontend/search.html` (구현 예정)
- 여행지 검색 페이지
- 필터 (테마, 가족 구성, 예산 등)
- 검색 결과 표시

#### `frontend/create-itinerary.html` (구현 예정)
- 여행 계획 생성 페이지
- 출발지, 목적지, 기간 입력
- 예산 설정
- 자동 일정 생성

#### `frontend/transportation.html` (구현 예정)
- 교통편 정보 페이지
- 장거리 교통 (QR 코드)
- 시내 교통 (QR 코드)
- 앱 다운로드 링크

#### `frontend/budget.html` (구현 예정)
- 예산 계산 페이지
- 항목별 예산
- 예산 요약
- 환율 계산

---

### 📚 문서 파일

#### `README.md`
- 프로젝트 개요
- 주요 기능
- 프로젝트 구조
- 기술 스택
- 설치 방법
- API 엔드포인트

#### `INSTALLATION_GUIDE.md`
- 상세 설치 절차
- 문제 해결
- 다음 단계

#### `.gitignore`
- Python 관련 파일
- IDE 파일
- 환경 변수 파일
- 데이터베이스 파일

---

### 🔄 구현 예정 파일

#### `backend/app/routers/users.py`
```python
# 사용자 관련 API
POST   /api/v1/users/register
POST   /api/v1/users/login
GET    /api/v1/users/me
PUT    /api/v1/users/profile
```

#### `backend/app/routers/destinations.py`
```python
# 여행지 관련 API
GET    /api/v1/destinations
GET    /api/v1/destinations/{id}
POST   /api/v1/destinations/search
GET    /api/v1/destinations/recommend
```

#### `backend/app/routers/itineraries.py`
```python
# 여행 일정 관련 API
POST   /api/v1/itineraries
GET    /api/v1/itineraries
GET    /api/v1/itineraries/{id}
PUT    /api/v1/itineraries/{id}
DELETE /api/v1/itineraries/{id}
```

#### `backend/app/routers/transportation.py`
```python
# 교통편 관련 API
GET    /api/v1/transportation/long-distance/search
GET    /api/v1/transportation/local/{id}
GET    /api/v1/qr-codes/{category}/{id}
```

#### `backend/app/routers/budgets.py`
```python
# 예산 관련 API
GET    /api/v1/itineraries/{id}/budgets
POST   /api/v1/itineraries/{id}/budgets
PUT    /api/v1/budgets/{id}
GET    /api/v1/itineraries/{id}/budget-summary
```

---

## 📝 파일 크기 요약

| 파일 | 크기 |
|------|------|
| models.py | ~10KB |
| schemas.py | ~8.5KB |
| main.py | ~2.6KB |
| auth.py | ~3KB |
| database.py | ~1.3KB |
| qr_generator.py | ~5KB |
| index.html | ~9.4KB |
| style.css | ~8KB |
| script.js | ~7.7KB |
| requirements.txt | ~0.5KB |

**총 크기**: ~55KB (매우 가벼움)

---

## 🚀 빠른 시작 명령어

```bash
# 1. 프로젝트 설정
cd travel-planner
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 또는
venv\Scripts\activate  # Windows

# 2. 패키지 설치
cd backend
pip install -r requirements.txt

# 3. 환경 변수 설정
cp .env.example .env
# .env 파일 수정 (DATABASE_URL, SECRET_KEY 등)

# 4. 데이터베이스 생성
# PostgreSQL 실행 후 데이터베이스 생성

# 5. 서버 실행
python -m app.main

# 6. 브라우저에서 확인
# http://localhost:8000
# http://localhost:8000/docs (API 문서)
```

---

## ✅ 체크리스트

- [ ] 디렉토리 구조 생성
- [ ] 모든 파일 복사/생성
- [ ] requirements.txt 설치
- [ ] .env 파일 설정
- [ ] PostgreSQL 설정
- [ ] 서버 실행 테스트
- [ ] http://localhost:8000 접속 확인
- [ ] http://localhost:8000/docs API 문서 확인

---

## 🎯 다음 단계

1. **API Routers 구현** (Task #3-7)
   - 사용자 관련 API
   - 여행지 검색/추천
   - 일정 생성
   - 교통편 정보
   - 예산 계산

2. **프론트엔드 페이지 완성** (Task #8)
   - search.html
   - create-itinerary.html
   - transportation.html
   - budget.html

3. **통합 테스트** (Task #9)
   - API 테스트
   - 프론트엔드 통합 테스트

---

## 💡 팁

- VS Code에서 Python Extension 설치 권장
- REST Client 확장으로 API 테스트 가능
- Live Server 확장으로 HTML 파일 실시간 보기
- SQLAlchemy 모델이 이미 완성되어 있으니, 라우터만 구현하면 됨!

---

**준비 완료! 이제 시작해봅시다! 🚀**
