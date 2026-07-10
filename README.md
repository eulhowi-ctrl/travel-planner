# 🌍 Travel Planner - AI-Powered Travel Planning Application

여행 계획을 자동으로 생성해주는 AI 기반 웹 애플리케이션입니다.

[English](#english) | [한국어](#korean)

---

## 한국어 <a name="korean"></a>

### 📋 개요

Travel Planner는 사용자의 여행 스타일과 선호도에 맞춰 여행 계획을 자동으로 생성하고 관리하는 웹 애플리케이션입니다.

**주요 기능:**
- 🔐 안전한 사용자 인증 (JWT 기반)
- 🎯 개인화된 여행지 추천 (테마/활동 기반)
- 📅 자동 일정 생성 (일별 활동 및 일정)
- 💰 예산 관리 및 추적
- 💱 실시간 환율 변환
- 🚗 교통 정보 통합 (비행, 기차, 버스, 택시)
- 🎫 QR 코드 생성 (예약, WiFi, 연락처)

### 🚀 빠른 시작

**Docker Compose 사용 (권장):**

```bash
# 1. 저장소 클론
git clone <repository-url>
cd travel-planner

# 2. 환경 설정
cp backend/.env.example backend/.env

# 3. 애플리케이션 시작
docker-compose up -d

# 4. 웹 브라우저에서 접속
# 웹사이트: http://localhost
# API 문서: http://localhost:8000/docs
```

### 🏗️ 기술 스택

- **FastAPI** - 현대적인 Python 웹 프레임워크
- **PostgreSQL** - 관계형 데이터베이스
- **SQLAlchemy** - ORM
- **JWT** - 인증
- **Docker** - 컨테이너화
- **Nginx** - 웹 서버

### 📚 API 엔드포인트

- `POST /api/v1/users/register` - 회원가입
- `POST /api/v1/auth/login` - 로그인
- `POST /api/v1/destinations/search` - 여행지 검색
- `POST /api/v1/itineraries` - 여행 계획 생성
- `POST /api/v1/budgets` - 예산 추가
- `GET /api/v1/qr-codes/generate` - QR 코드 생성

### 📖 문서

- [QUICKSTART.md](QUICKSTART.md) - 빠른 시작
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - 배포 가이드
- [backend/INTEGRATION_TEST_GUIDE.md](backend/INTEGRATION_TEST_GUIDE.md) - 테스트

---

## English <a name="english"></a>

### 📋 Overview

Travel Planner is a web application that automatically generates and manages travel plans based on user preferences and travel style.

**Key Features:**
- 🔐 Secure authentication (JWT-based)
- 🎯 Personalized destination recommendations
- 📅 Automatic itinerary generation
- 💰 Budget management and tracking
- 💱 Real-time currency conversion
- 🚗 Integrated transportation information
- 🎫 QR code generation

### 🚀 Quick Start

**Using Docker Compose (Recommended):**

```bash
# 1. Clone repository
git clone <repository-url>
cd travel-planner

# 2. Configure environment
cp backend/.env.example backend/.env

# 3. Start application
docker-compose up -d

# 4. Open in browser
# Website: http://localhost
# API Docs: http://localhost:8000/docs
```

### 🏗️ Tech Stack

- FastAPI - Modern Python web framework
- PostgreSQL - Relational database
- SQLAlchemy - ORM
- JWT - Authentication
- Docker - Containerization
- Nginx - Web server

### 📚 API Endpoints

- `POST /api/v1/users/register` - User registration
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/destinations/search` - Search destinations
- `POST /api/v1/itineraries` - Create travel plan
- `POST /api/v1/budgets` - Add budget item
- `GET /api/v1/qr-codes/generate` - Generate QR code

### 📖 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Quick start guide
- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Deployment guide
- [backend/INTEGRATION_TEST_GUIDE.md](backend/INTEGRATION_TEST_GUIDE.md) - Testing

---

**Created with ❤️ for travel enthusiasts**
