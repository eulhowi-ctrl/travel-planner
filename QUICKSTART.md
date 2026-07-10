# Quick Start Guide - 여행 계획 애플리케이션

여행 계획 애플리케이션을 빠르게 시작하는 가이드입니다.

## 사전 요구사항

- Docker & Docker Compose가 설치되어 있어야 합니다
- 또는: Python 3.11+, PostgreSQL 16+

## 방법 1: Docker Compose로 시작 (가장 쉬움)

### 1단계: 저장소 준비
```bash
cd travel-planner
```

### 2단계: 환경 변수 설정
```bash
cp backend/.env.example backend/.env
```

### 3단계: 애플리케이션 시작
```bash
docker-compose up -d
```

### 4단계: 접속
- **웹 사이트**: http://localhost
- **API 문서**: http://localhost:8000/docs
- **API ReDoc**: http://localhost:8000/redoc

## 방법 2: 로컬 개발 환경

### 백엔드 설정

```bash
cd backend

# 1. 가상 환경 생성
python3 -m venv venv
source venv/bin/activate

# 2. 패키지 설치
pip install -r requirements.txt

# 3. PostgreSQL 시작 (Docker)
docker run -d \
  --name travel-db \
  -e POSTGRES_USER=travel_user \
  -e POSTGRES_PASSWORD=travel_password_123 \
  -e POSTGRES_DB=travel_planner_db \
  -p 5432:5432 \
  postgres:16-alpine

# 4. 백엔드 서버 시작
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 프론트엔드 설정

```bash
cd frontend

# Python 내장 서버로 프론트엔드 서빙
python3 -m http.server 3000
```

그 다음 http://localhost:3000 에 접속

## 테스트

### API 헬스 체크
```bash
curl http://localhost:8000/api/v1/health
```

### 사용자 등록
```bash
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "full_name": "테스트 사용자"
  }'
```

### 더 많은 테스트
`INTEGRATION_TEST_GUIDE.md` 참고

## 주요 기능

✅ 사용자 인증 (회원가입, 로그인)
✅ 여행지 검색 및 추천
✅ 여행 계획 자동 생성
✅ 일별 일정 자동 생성
✅ 예산 관리 및 추적
✅ 환율 변환
✅ 교통 정보 (비행, 기차, 버스, 택시)
✅ QR 코드 생성

## 주요 파일

- `backend/app/` - FastAPI 백엔드
- `frontend/` - HTML/CSS/JavaScript 프론트엔드
- `docker-compose.yml` - Docker 설정
- `Dockerfile` - 백엔드 이미지
- `nginx.conf` - 웹 서버 설정

## 문제 해결

### Docker 오류
```bash
# 모든 서비스 상태 확인
docker-compose ps

# 로그 보기
docker-compose logs -f api
docker-compose logs -f postgres

# 재시작
docker-compose restart
```

### 포트 충돌
`docker-compose.yml`에서 포트 변경:
```yaml
ports:
  - "8080:8000"  # 8080으로 변경
```

### 데이터베이스 초기화
```bash
docker-compose down -v
docker-compose up -d
```

## API 문서

- `DESTINATIONS_API_GUIDE.md` - 여행지 API
- `TRANSPORTATION_API_GUIDE.md` - 교통 API
- `QR_CODE_API_GUIDE.md` - QR 코드 API
- `INTEGRATION_TEST_GUIDE.md` - 통합 테스트

## 다음 단계

1. **회원가입**: http://localhost에서 계정 생성
2. **프로필 작성**: 여행 스타일 선택
3. **목적지 검색**: 다양한 필터로 여행지 검색
4. **여행 계획**: 자동으로 일정 생성
5. **예산 관리**: 비용 추적 및 통화 변환
6. **예약**: QR 코드로 쉽게 예약

## 지원

문제가 생기면:
1. 로그 확인: `docker-compose logs -f`
2. 헬스 체크: `curl http://localhost:8000/api/v1/health`
3. API 문서 확인: http://localhost:8000/docs
