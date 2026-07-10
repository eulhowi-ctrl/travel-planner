# 🚀 Travel Planner - 설치 및 실행 가이드

## 📂 프로젝트 구조

```
travel-planner/
├── backend/                                  # FastAPI 백엔드
│   ├── app/
│   │   ├── __init__.py                      # 패키지 초기화
│   │   ├── main.py                          # FastAPI 애플리케이션 진입점
│   │   ├── models.py                        # SQLAlchemy 데이터베이스 모델
│   │   │   ├── User (사용자)
│   │   │   ├── UserProfile (사용자 프로필 - 테마, 선호도)
│   │   │   ├── Destination (여행지)
│   │   │   ├── LongDistanceTransportation (항공/기차/버스)
│   │   │   ├── LocalTransportation (시내 버스/지하철/택시)
│   │   │   ├── Itinerary (여행 일정)
│   │   │   ├── ItineraryDay (일정 내 각 일자)
│   │   │   ├── Budget (예산)
│   │   │   └── QRCode (생성된 QR 코드)
│   │   ├── schemas.py                       # Pydantic 데이터 검증 스키마
│   │   ├── database.py                      # 데이터베이스 연결 설정
│   │   ├── auth.py                          # JWT 인증 로직
│   │   ├── routers/                         # API 라우터 (구현 예정)
│   │   │   ├── users.py                     # 사용자 관련 API
│   │   │   ├── destinations.py              # 여행지 검색 및 추천
│   │   │   ├── itineraries.py               # 일정 생성 및 관리
│   │   │   ├── transportation.py            # 교통편 정보
│   │   │   └── budgets.py                   # 예산 계산
│   │   └── utils/
│   │       └── qr_generator.py              # QR 코드 생성 유틸리티
│   ├── requirements.txt                     # Python 패키지 의존성
│   ├── .env.example                         # 환경 변수 예시 파일
│   └── .env                                 # 환경 변수 (실제 설정)
│
├── frontend/                                # HTML/CSS/JS 프론트엔드
│   ├── index.html                           # 홈페이지 (✅ 완성)
│   ├── search.html                          # 여행지 검색 (구현 예정)
│   ├── create-itinerary.html                # 일정 생성 (구현 예정)
│   ├── transportation.html                  # 교통편 정보 (구현 예정)
│   ├── budget.html                          # 예산 계산 (구현 예정)
│   ├── style.css                            # 전체 스타일시트 (✅ 완성)
│   └── script.js                            # 공통 JavaScript (✅ 완성)
│
├── static/                                  # 정적 파일 (자동 생성)
│   └── qr_codes/                            # 생성된 QR 코드 이미지
│
├── README.md                                # 프로젝트 설명
├── INSTALLATION_GUIDE.md                    # 이 파일 (설치 가이드)
└── .gitignore                               # Git 무시 파일 (구현 예정)
```

---

## 📋 완성된 파일 체크리스트

✅ **Backend (완성)**
- [x] `models.py` - 전체 데이터베이스 모델
- [x] `schemas.py` - 모든 Pydantic 스키마
- [x] `database.py` - 데이터베이스 연결 설정
- [x] `auth.py` - JWT 인증 로직
- [x] `main.py` - FastAPI 애플리케이션
- [x] `qr_generator.py` - QR 코드 생성 유틸리티
- [x] `requirements.txt` - 필요한 패키지

✅ **Frontend (홈페이지 완성)**
- [x] `index.html` - 홈페이지 및 기본 구조
- [x] `style.css` - 전체 스타일시트 (반응형)
- [x] `script.js` - 공통 JavaScript 함수

⏳ **Frontend (구현 예정)**
- [ ] `search.html` - 여행지 검색 페이지
- [ ] `create-itinerary.html` - 일정 생성 페이지
- [ ] `transportation.html` - 교통편 정보 페이지
- [ ] `budget.html` - 예산 계산 페이지

⏳ **Backend API Routers (구현 예정)**
- [ ] `routers/users.py` - 사용자 관련 API
- [ ] `routers/destinations.py` - 여행지 검색/추천 API
- [ ] `routers/itineraries.py` - 일정 생성/관리 API
- [ ] `routers/transportation.py` - 교통편 정보 API
- [ ] `routers/budgets.py` - 예산 계산 API

---

## 🛠️ 설치 절차

### 1️⃣ 사전 요구사항

```bash
# 설치 필요 항목:
- Python 3.8 이상
- PostgreSQL (또는 SQLite 사용 가능)
- Git
```

### 2️⃣ 프로젝트 설정

```bash
# 프로젝트 디렉토리로 이동
cd travel-planner

# Python 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
# Windows:
venv\Scripts\activate

# macOS/Linux:
source venv/bin/activate

# 백엔드 디렉토리로 이동
cd backend

# 필요한 패키지 설치
pip install -r requirements.txt

# 프론트엔드로 이동 (선택사항)
cd ../frontend
# HTML 파일들을 웹 서버로 제공하거나, VS Code의 Live Server 사용
```

### 3️⃣ 환경 변수 설정

```bash
cd backend

# .env.example에서 .env 생성
cp .env.example .env

# .env 파일 편집 (중요!)
# DATABASE_URL=postgresql://user:password@localhost:5432/travel_planner_db
# SECRET_KEY=your-very-secret-key-here (production에서는 보안 강화)
# DEBUG=True (개발 중에만)
```

### 4️⃣ 데이터베이스 설정

**옵션 A: PostgreSQL 사용 (권장)**

```bash
# PostgreSQL 설치 후 데이터베이스 생성
# macOS (Homebrew):
brew install postgresql
brew services start postgresql

# 또는 Docker 사용:
docker run -d \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=travel_planner_db \
  -p 5432:5432 \
  postgres:15
```

**옵션 B: SQLite 사용 (간단)**

```bash
# .env 파일에서:
DATABASE_URL=sqlite:///./travel_planner.db
```

### 5️⃣ 서버 실행

```bash
cd backend

# FastAPI 서버 시작
python -m app.main

# 또는 Uvicorn 직접 실행:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 6️⃣ 브라우저에서 확인

```
주소: http://localhost:8000

주요 링크:
- 홈페이지: http://localhost:8000
- API 문서: http://localhost:8000/docs
- 상태 확인: http://localhost:8000/health
```

---

## 🚀 다음 단계

### 1단계: API Routers 구현

다음 파일들을 생성해야 합니다:

```bash
backend/app/routers/
├── users.py              # 회원가입, 로그인, 프로필 관리
├── destinations.py       # 여행지 검색, 테마별 추천
├── itineraries.py        # 일정 생성, 조회, 수정
├── transportation.py     # 교통편 정보 (장거리/시내)
└── budgets.py           # 예산 계산 및 조회
```

### 2단계: 프론트엔드 페이지 구현

```bash
frontend/
├── search.html              # 여행지 검색 페이지
├── create-itinerary.html    # 일정 생성 페이지
├── transportation.html      # 교통편 정보 페이지
└── budget.html             # 예산 계산 페이지
```

### 3단계: 데이터베이스 초기 데이터

다음 정보들을 데이터베이스에 입력해야 합니다:

- 주요 여행지 정보 (이름, 위치, 테마 등)
- 교통편 기본 정보
- 시내 교통 정보

---

## 📚 API 엔드포인트 (구현할 것들)

### 사용자 API
```
POST   /api/v1/users/register          # 회원가입
POST   /api/v1/users/login             # 로그인
GET    /api/v1/users/me                # 내 정보
PUT    /api/v1/users/profile           # 프로필 수정
```

### 여행지 API
```
GET    /api/v1/destinations            # 여행지 목록
GET    /api/v1/destinations/{id}       # 상세 정보
POST   /api/v1/destinations/search     # 검색
GET    /api/v1/destinations/recommend  # 맞춤형 추천
```

### 교통편 API
```
GET    /api/v1/transportation/long-distance/search
GET    /api/v1/transportation/local/{id}
GET    /api/v1/qr-codes/{category}/{id}
```

### 일정 API
```
POST   /api/v1/itineraries             # 생성
GET    /api/v1/itineraries             # 조회
PUT    /api/v1/itineraries/{id}        # 수정
DELETE /api/v1/itineraries/{id}        # 삭제
```

### 예산 API
```
GET    /api/v1/itineraries/{id}/budgets
POST   /api/v1/itineraries/{id}/budgets
PUT    /api/v1/budgets/{id}
GET    /api/v1/itineraries/{id}/budget-summary
```

---

## 🔧 문제 해결

### PostgreSQL 연결 오류
```
오류: could not connect to server: Connection refused
해결: PostgreSQL이 실행 중인지 확인
brew services start postgresql  # macOS
```

### 모듈 import 오류
```
오류: ModuleNotFoundError: No module named 'app'
해결: backend 디렉토리에서 실행 확인
cd backend
python -m app.main
```

### 포트 이미 사용 중
```
오류: Address already in use
해결: 다른 포트 사용
uvicorn app.main:app --port 8001
```

---

## 📞 지원

문제가 있거나 질문이 있으신가요?
- 에러 메시지를 확인하세요 (매우 구체적입니다)
- README.md를 다시 읽어보세요
- FastAPI 공식 문서: https://fastapi.tiangolo.com

---

## 🎉 행운을 빕니다!

이제 준비 완료! 멋진 여행 계획 애플리케이션을 만들어봅시다! ✈️🌍
