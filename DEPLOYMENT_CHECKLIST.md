# 🚀 Deployment Checklist - Travel Planner

배포 전 확인 사항 및 단계별 배포 가이드입니다.

---

## ✅ 배포 전 체크리스트

### 1. 코드 검증
- [x] 모든 Python 파일 구문 검사
- [x] 모든 HTML 파일 검증
- [x] JavaScript 오류 확인
- [x] 데이터베이스 마이그레이션 준비
- [x] 환경 변수 템플릿 생성 (.env.example)

### 2. 의존성 확인
- [x] requirements.txt 최신 상태
- [x] Docker 이미지 빌드 가능
- [x] PostgreSQL 호환성 확인
- [x] Python 3.11+ 호환성
- [x] Node.js 의존성 없음 (순수 HTML/JS)

### 3. 보안 검토
- [x] JWT 토큰 설정
- [x] 비밀번호 해싱 (Bcrypt)
- [x] CORS 정책 설정
- [x] SQL Injection 방지 (ORM 사용)
- [x] 환경 변수 민감 정보 보호

### 4. 문서 완성
- [x] README.md (영문/한국어)
- [x] QUICKSTART.md
- [x] DEPLOYMENT_GUIDE.md
- [x] INTEGRATION_TEST_GUIDE.md
- [x] API 문서 (3개)
- [x] .gitignore
- [x] Dockerfile
- [x] docker-compose.yml

### 5. 데이터베이스
- [x] SQLAlchemy 모델 정의
- [x] 마이그레이션 스크립트
- [x] 샘플 데이터 생성
- [x] 외래키 관계 설정
- [x] 인덱스 설계

---

## 🔧 로컬 배포 (개발)

### Step 1: 환경 준비
```bash
# 1a. Python 3.11+ 설치 확인
python3 --version

# 1b. Docker & Docker Compose 설치 (선택)
docker --version
docker-compose --version
```

### Step 2: 프로젝트 설정
```bash
# 2a. 저장소 클론
git clone <repository-url>
cd travel-planner

# 2b. 환경 변수 설정
cp backend/.env.example backend/.env

# .env 파일 편집 (필요시)
# - DATABASE_URL: PostgreSQL 연결 주소
# - SECRET_KEY: JWT 비밀 키 (강력한 난수)
# - DEBUG: False (프로덕션에서)
```

### Step 3: 백엔드 시작
```bash
# 3a. 가상 환경 생성
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는: venv\Scripts\activate  # Windows

# 3b. 패키지 설치
pip install -r requirements.txt

# 3c. PostgreSQL 시작 (Docker)
docker run -d \
  --name travel-db \
  -e POSTGRES_USER=travel_user \
  -e POSTGRES_PASSWORD=travel_password_123 \
  -e POSTGRES_DB=travel_planner_db \
  -p 5432:5432 \
  postgres:16-alpine

# 3d. 서버 시작
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: 프론트엔드 시작
```bash
# 4a. 새 터미널에서
cd frontend

# 4b. Python 서버로 정적 파일 서빙
python3 -m http.server 3000

# 또는 Nginx 사용
sudo nginx -c /path/to/nginx.conf
```

### Step 5: 접속 확인
- 웹사이트: http://localhost:3000
- API: http://localhost:8000
- API 문서: http://localhost:8000/docs

---

## 🐳 Docker 배포 (권장)

### Step 1: Docker 설치 확인
```bash
docker --version
docker-compose --version
```

### Step 2: 환경 설정
```bash
cp backend/.env.example backend/.env

# .env 파일 편집
# DATABASE_URL=postgresql://travel_user:travel_password_123@postgres:5432/travel_planner_db
# SECRET_KEY=<매우-강력한-난수>
```

### Step 3: Docker Compose 실행
```bash
# 이미지 빌드 및 컨테이너 시작
docker-compose up -d

# 상태 확인
docker-compose ps

# 로그 확인
docker-compose logs -f api
docker-compose logs -f postgres
```

### Step 4: 접속 확인
```bash
# 헬스 체크
curl http://localhost:8000/api/v1/health

# 웹사이트
open http://localhost

# API 문서
open http://localhost:8000/docs
```

### Step 5: 데이터 확인
```bash
# PostgreSQL 접속
docker-compose exec postgres psql -U travel_user -d travel_planner_db

# 테이블 확인
\dt

# 샘플 데이터 확인
SELECT COUNT(*) FROM destinations;
SELECT COUNT(*) FROM users;
```

---

## ☁️ 클라우드 배포

### AWS ECS 배포

#### 1단계: ECR에 이미지 푸시
```bash
# AWS 자격증명 설정
aws configure

# ECR 저장소 생성
aws ecr create-repository --repository-name travel-planner

# ECR 로그인
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# 이미지 빌드 및 푸시
docker build -t travel-planner:latest .
docker tag travel-planner:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/travel-planner:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/travel-planner:latest
```

#### 2단계: RDS 데이터베이스 생성
```bash
# AWS Console에서 RDS PostgreSQL 생성
# 또는 AWS CLI로 생성
aws rds create-db-instance \
  --db-instance-identifier travel-planner-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username travel_user \
  --master-user-password <strong-password>
```

#### 3단계: ECS 작업 정의 생성
```bash
# task-definition.json 생성
# environment 변수 설정:
# - DATABASE_URL=postgresql://...
# - SECRET_KEY=...
```

#### 4단계: ECS 서비스 생성
```bash
aws ecs create-service \
  --cluster travel-planner-cluster \
  --service-name travel-planner-service \
  --task-definition travel-planner:1
```

### Google Cloud Run 배포

```bash
# 1. GCP 프로젝트 설정
gcloud auth login
gcloud config set project <PROJECT_ID>

# 2. 이미지 빌드 및 푸시
gcloud builds submit --tag gcr.io/<PROJECT_ID>/travel-planner

# 3. Cloud Run 배포
gcloud run deploy travel-planner \
  --image gcr.io/<PROJECT_ID>/travel-planner \
  --platform managed \
  --region us-central1 \
  --memory 512Mi \
  --cpu 1 \
  --set-env-vars "DATABASE_URL=postgresql://...,SECRET_KEY=..."

# 4. 자동 스케일링 설정
gcloud run services update travel-planner \
  --max-instances 10 \
  --min-instances 1
```

### Heroku 배포

```bash
# 1. Heroku CLI 설치 및 로그인
heroku login

# 2. Heroku 앱 생성
heroku create travel-planner

# 3. PostgreSQL 추가
heroku addons:create heroku-postgresql:standard-0

# 4. 환경 변수 설정
heroku config:set SECRET_KEY="<strong-key>"
heroku config:set DEBUG=False

# 5. 배포
git push heroku main

# 6. 로그 확인
heroku logs --tail
```

---

## 🧪 배포 후 테스트

### Step 1: 기본 테스트
```bash
# 헬스 체크
curl http://<your-domain>/api/v1/health

# 응답:
# {
#   "status": "healthy",
#   "api": "Travel Planner API",
#   "version": "1.0.0",
#   "timestamp": "2026-07-10T12:00:00"
# }
```

### Step 2: 사용자 테스트
```bash
# 회원가입
curl -X POST http://<your-domain>/api/v1/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Password123!",
    "full_name": "Test User"
  }'

# 로그인
curl -X POST http://<your-domain>/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=Password123!"

# 응답에서 access_token 저장
```

### Step 3: API 테스트
```bash
# 여행지 검색 (토큰 필요)
curl -X POST http://<your-domain>/api/v1/destinations/search \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "제주도",
    "skip": 0,
    "limit": 10
  }'

# 자세한 테스트는 INTEGRATION_TEST_GUIDE.md 참고
```

### Step 4: 프론트엔드 테스트
1. 브라우저에서 http://<your-domain> 접속
2. 계정 생성
3. 로그인
4. 여행지 검색
5. 여행 계획 생성
6. 예산 관리 확인

---

## 📊 모니터링 설정

### 로그 모니터링
```bash
# Docker Compose
docker-compose logs -f

# Heroku
heroku logs --tail

# AWS CloudWatch
aws logs tail /aws/ecs/travel-planner --follow

# GCP Cloud Logging
gcloud logging read "resource.type=cloud_run_revision" --limit 10
```

### 성능 모니터링
```bash
# Docker 리소스 사용
docker stats

# PostgreSQL 연결 수
docker-compose exec postgres \
  psql -U travel_user -d travel_planner_db \
  -c "SELECT count(*) FROM pg_stat_activity;"
```

### 알림 설정

#### AWS CloudWatch
```bash
aws cloudwatch put-metric-alarm \
  --alarm-name travel-planner-high-cpu \
  --alarm-description "Alert when CPU usage is high" \
  --metric-name CPUUtilization \
  --namespace AWS/ECS \
  --statistic Average \
  --period 300 \
  --threshold 80 \
  --comparison-operator GreaterThanThreshold
```

#### Heroku
```bash
# Heroku 대시보드에서 "Alerts" 설정
# dyno 오류율, 응답 시간 등 모니터링
```

---

## 🔄 운영 가이드

### 정기 유지보수
- 주 1회: 로그 검토
- 월 1회: 데이터베이스 최적화
- 월 1회: 의존성 업데이트 확인
- 분기 1회: 보안 감시

### 백업 전략
```bash
# PostgreSQL 백업
docker-compose exec postgres \
  pg_dump -U travel_user travel_planner_db > backup.sql

# 자동 백업 설정 (크론 작업)
# 0 2 * * * /path/to/backup.sh
```

### 스케일링
- **수직 스케일링**: 더 큰 인스턴스 사용
- **수평 스케일링**: 로드 밸런서 + 여러 인스턴스
- **데이터베이스**: 읽기 복제본 추가

### 업데이트
```bash
# 코드 업데이트
git pull origin main
docker-compose build --no-cache
docker-compose up -d

# 데이터베이스 마이그레이션
docker-compose exec api alembic upgrade head
```

---

## ❌ 문제 해결

### 포트 충돌
```bash
# 사용 중인 포트 확인
lsof -i :8000
lsof -i :5432

# 포트 변경 (docker-compose.yml)
ports:
  - "8080:8000"  # 8080으로 변경
```

### 데이터베이스 연결 오류
```bash
# 1. PostgreSQL 상태 확인
docker-compose ps postgres

# 2. 연결 테스트
docker-compose exec postgres \
  pg_isready -U travel_user -d travel_planner_db

# 3. 로그 확인
docker-compose logs postgres

# 4. 재시작
docker-compose restart postgres
```

### 메모리 부족
```bash
# 1. 리소스 사용 확인
docker stats

# 2. docker-compose.yml에서 제한 설정
deploy:
  resources:
    limits:
      memory: 512M
    reservations:
      memory: 256M

# 3. 불필요한 컨테이너 정리
docker system prune
```

### API 오류
```bash
# 1. 헬스 체크
curl http://localhost:8000/api/v1/health

# 2. 로그 확인
docker-compose logs api

# 3. API 문서 확인
http://localhost:8000/docs

# 4. 환경 변수 확인
docker-compose exec api env | grep DATABASE
```

---

## ✅ 배포 완료 체크리스트

- [ ] 로컬 환경에서 테스트 완료
- [ ] 도메인 DNS 설정
- [ ] SSL/TLS 인증서 설치
- [ ] 환경 변수 설정 (프로덕션)
- [ ] 백업 전략 수립
- [ ] 모니터링 설정
- [ ] 로깅 시스템 구성
- [ ] 성능 최적화 완료
- [ ] 보안 감사 완료
- [ ] 사용자 문서 준비
- [ ] 팀 교육 완료
- [ ] 배포 후 검증

---

## 📞 지원

문제가 발생하면:
1. 로그 확인: `docker-compose logs -f`
2. 헬스 체크: `curl http://localhost:8000/api/v1/health`
3. 문서 참고: `INTEGRATION_TEST_GUIDE.md`
4. GitHub Issues 검색
5. 관리자에게 연락

---

**배포 성공을 기원합니다! 🚀**
