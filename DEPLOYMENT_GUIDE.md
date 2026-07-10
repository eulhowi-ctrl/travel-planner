# Travel Planner - Deployment Guide

이 가이드는 여행 계획 애플리케이션을 배포하고 실행하는 방법을 설명합니다.

## 시스템 요구사항

- Docker & Docker Compose
- 또는 Python 3.11+, PostgreSQL 16+, Node.js (프론트엔드)

## 배포 방법

### 방법 1: Docker Compose (권장)

가장 간단한 방법으로 Docker와 Docker Compose만으로 전체 애플리케이션을 실행합니다.

#### 준비 단계

1. 저장소 클론
```bash
git clone <repository-url>
cd travel-planner
```

2. 환경 변수 설정
```bash
cp backend/.env.example backend/.env
```

`.env` 파일 편집:
```
DATABASE_URL=postgresql://travel_user:travel_password_123@postgres:5432/travel_planner_db
SECRET_KEY=your-very-secure-key-change-in-production-12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=False
```

#### 실행

3. Docker Compose로 실행
```bash
# 이미지 빌드 및 서비스 시작
docker-compose up -d

# 또는 로그를 보면서 실행 (개발 모드)
docker-compose up
```

4. 상태 확인
```bash
# 서비스 상태 확인
docker-compose ps

# API 헬스 체크
curl http://localhost:8000/api/v1/health

# 로그 확인
docker-compose logs -f api
docker-compose logs -f postgres
```

#### 접근

- **프론트엔드**: http://localhost:80 (또는 http://localhost)
- **API 문서**: http://localhost:8000/docs (Swagger UI)
- **API 재문서**: http://localhost:8000/redoc (ReDoc)
- **건강 상태**: http://localhost:8000/api/v1/health

### 방법 2: 로컬 개발 환경 설정

Python 환경에서 직접 실행하는 방법입니다.

#### 백엔드 설정

1. Python 3.11 설치 확인
```bash
python3 --version
```

2. 가상 환경 생성
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows
```

3. 패키지 설치
```bash
pip install -r requirements.txt
```

4. PostgreSQL 설치 및 실행
```bash
# macOS (Homebrew 사용)
brew install postgresql@16
brew services start postgresql@16

# Linux (Ubuntu/Debian)
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql

# 또는 Docker로 실행
docker run -d \
  --name postgres-travel \
  -e POSTGRES_USER=travel_user \
  -e POSTGRES_PASSWORD=travel_password_123 \
  -e POSTGRES_DB=travel_planner_db \
  -p 5432:5432 \
  postgres:16-alpine
```

5. 데이터베이스 초기화
```bash
createdb -U travel_user travel_planner_db
```

6. 환경 변수 설정
```bash
cp .env.example .env
# 필요시 .env 편집
```

7. 백엔드 서버 시작
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 프론트엔드 설정

1. Node.js 기반 개발 서버 (선택사항)
```bash
cd frontend
# Python 간단한 서버로 실행
python3 -m http.server 3000
```

또는 nginx/Apache로 정적 파일 서빙

## 테스트

### 통합 테스트 실행

백엔드 서버가 실행 중이어야 합니다.

```bash
cd backend
bash INTEGRATION_TEST_GUIDE.md
```

자세한 테스트 가이드는 `INTEGRATION_TEST_GUIDE.md` 참고

### API 엔드포인트 검증

```bash
# 헬스 체크
curl http://localhost:8000/api/v1/health

# 사용자 등록
curl -X POST http://localhost:8000/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "password123",
    "full_name": "Test User"
  }'

# 로그인
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=password123"

# API 문서 확인
curl http://localhost:8000/docs
```

## 프로덕션 배포

### 클라우드 배포 옵션

#### AWS (ECS/Fargate)

1. ECR에 이미지 푸시
```bash
# AWS CLI 설치 및 인증
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# 이미지 빌드 및 푸시
docker build -t travel-planner:latest .
docker tag travel-planner:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/travel-planner:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/travel-planner:latest
```

2. ECS 작업 정의 생성 및 서비스 배포

#### Google Cloud Run

```bash
# GCP 프로젝트 설정
gcloud auth login
gcloud config set project <PROJECT_ID>

# 이미지 빌드 및 푸시
gcloud builds submit --tag gcr.io/<PROJECT_ID>/travel-planner

# Cloud Run에 배포
gcloud run deploy travel-planner \
  --image gcr.io/<PROJECT_ID>/travel-planner \
  --platform managed \
  --region us-central1 \
  --set-env-vars "DATABASE_URL=postgresql://...,SECRET_KEY=..."
```

#### Heroku

```bash
# Heroku CLI 설치 및 로그인
heroku login

# Heroku 앱 생성
heroku create travel-planner

# PostgreSQL 추가
heroku addons:create heroku-postgresql:standard-0

# 환경 변수 설정
heroku config:set SECRET_KEY="your-secret-key"

# 배포
git push heroku main
```

### 환경 변수 설정 (프로덕션)

프로덕션 환경에서는 다음을 변경하세요:

```env
# 보안
DEBUG=False
SECRET_KEY=<매우-강력한-난수-키>

# 데이터베이스
DATABASE_URL=postgresql://user:password@db-host:5432/travel_planner_db

# API
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# SSL/TLS (nginx에서 처리 가능)
# 또는 Let's Encrypt 인증서 사용
```

### 모니터링 및 로깅

```bash
# Docker 컨테이너 로그
docker-compose logs -f api

# 애플리케이션 로그 (마운트된 볼륨)
tail -f logs/travel-planner.log

# 성능 모니터링
docker stats

# 헬스 체크 모니터링
watch -n 30 'curl -s http://localhost:8000/api/v1/health'
```

## 업데이트

### 코드 업데이트

```bash
# 최신 변경사항 가져오기
git pull origin main

# Docker 이미지 재빌드
docker-compose build --no-cache

# 서비스 재시작
docker-compose up -d
```

### 데이터베이스 마이그레이션

```bash
# Alembic 마이그레이션 실행
docker-compose exec api alembic upgrade head
```

## 문제 해결

### 포트 충돌

포트가 이미 사용 중인 경우 `docker-compose.yml`에서 변경:

```yaml
ports:
  - "8080:8000"  # 8080으로 변경
```

### 데이터베이스 연결 오류

```bash
# 데이터베이스 확인
docker-compose exec postgres psql -U travel_user -d travel_planner_db -c "\dt"

# 데이터베이스 재초기화
docker-compose down -v
docker-compose up -d
```

### 메모리/리소스 부족

`docker-compose.yml`에서 리소스 제한 조정:

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

## 보안 고려사항

1. **환경 변수**: 민감한 정보는 환경 변수로 관리
2. **HTTPS/TLS**: 프로덕션에서는 SSL 인증서 필수
3. **CORS**: 신뢰할 수 있는 도메인만 허용
4. **Rate Limiting**: API 엔드포인트에 요청 제한 추가
5. **인증**: JWT 토큰 만료 시간 설정 (기본: 30분)
6. **데이터베이스**: 정기적인 백업 수행

## 지원되는 API 엔드포인트

자세한 API 문서는 다음을 참고하세요:

- `DESTINATIONS_API_GUIDE.md` - 목적지 관련 엔드포인트
- `TRANSPORTATION_API_GUIDE.md` - 교통 관련 엔드포인트
- `QR_CODE_API_GUIDE.md` - QR 코드 생성 엔드포인트
- `TESTING_GUIDE.md` - 테스트 방법
- `INTEGRATION_TEST_GUIDE.md` - 통합 테스트

## 문의

문제가 발생하면 다음을 확인하세요:

1. 모든 서비스가 실행 중인지 확인: `docker-compose ps`
2. 로그 확인: `docker-compose logs -f`
3. 데이터베이스 연결 확인: `docker-compose exec postgres pg_isready`
4. API 헬스 체크: `curl http://localhost:8000/api/v1/health`
