# 📱 QR 코드 생성 API 가이드

## 🎯 개요

외부 API 기반의 QR 코드 생성 시스템으로 **라이브러리 의존성이 없습니다**.
- 별도의 서버 설치 불필요
- 실시간 생성 (캐싱 권장)
- 여러 포맷 지원 (PNG, JPG, SVG, WebP)

---

## 📚 API 엔드포인트 목록

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/v1/qr-codes/generate` | 기본 QR 코드 생성 |
| POST | `/api/v1/qr-codes/booking` | 예약 링크 QR 코드 |
| POST | `/api/v1/qr-codes/transportation` | 교통편 정보 QR 코드 |
| POST | `/api/v1/qr-codes/destination` | 여행지 정보 QR 코드 |
| POST | `/api/v1/qr-codes/app-download` | 앱 다운로드 QR 코드 |
| GET | `/api/v1/qr-codes/wifi` | WiFi 연결 QR 코드 |
| GET | `/api/v1/qr-codes/contact` | 연락처(vCard) QR 코드 |
| GET | `/api/v1/qr-codes/formats` | 지원 포맷 정보 |
| GET | `/api/v1/qr-codes/info` | API 정보 및 팁 |

---

## 🚀 API 사용 예시

### 1️⃣ 기본 QR 코드 생성

**요청:**
```bash
# URL을 QR 코드로 변환
curl -X GET "http://localhost:8000/api/v1/qr-codes/generate?data=https://www.koreanair.com&size=200&format_type=png"

# 텍스트를 QR 코드로 변환
curl -X GET "http://localhost:8000/api/v1/qr-codes/generate?data=제주도%20여행&size=250&format_type=svg"

# 전화번호를 QR 코드로 변환
curl -X GET "http://localhost:8000/api/v1/qr-codes/generate?data=tel:+82-2-123-4567"
```

**쿼리 파라미터:**
- `data`: QR 코드로 변환할 데이터 (필수)
- `size`: 크기 (50-1000, 기본값: 200)
- `format_type`: 포맷 (png/jpg/svg/webp, 기본값: png)

**성공 응답 (200):**
```json
{
  "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fwww.koreanair.com",
  "data": "https://www.koreanair.com",
  "size": "200",
  "format": "png"
}
```

**HTML에서 사용:**
```html
<img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fwww.koreanair.com" 
     alt="Korean Air" />
```

---

### 2️⃣ 예약 링크 QR 코드

**요청:**
```bash
curl -X POST "http://localhost:8000/api/v1/qr-codes/booking" \
  -H "Content-Type: application/json" \
  -d '{
    "booking_methods": [
      {
        "platform": "Official Website",
        "url": "https://www.koreanair.com",
        "how_to": "Direct booking"
      },
      {
        "platform": "Naver Travel",
        "url": "https://travel.naver.com",
        "how_to": "Online booking"
      }
    ]
  }'
```

**응답:**
```json
{
  "qr_codes": {
    "official_website": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fwww.koreanair.com",
    "naver_travel": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Ftravel.naver.com"
  },
  "total_codes": 2
}
```

---

### 3️⃣ 교통편 정보 QR 코드

**요청:**
```bash
curl -X POST "http://localhost:8000/api/v1/qr-codes/transportation" \
  -H "Content-Type: application/json" \
  -d '{
    "provider": "Korean Air",
    "departure_city": "서울",
    "arrival_city": "제주",
    "booking_methods": [
      {
        "platform": "Official Website",
        "url": "https://www.koreanair.com",
        "how_to": "Direct booking"
      }
    ]
  }'
```

**응답:**
```json
{
  "route_info": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=%EC%84%9C%EC%9A%B8+%E2%86%92+%EC%A0%9C%EC%A3%BC",
  "booking_links": {
    "official_website": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fwww.koreanair.com"
  }
}
```

---

### 4️⃣ 여행지 정보 QR 코드

**요청:**
```bash
curl -X POST "http://localhost:8000/api/v1/qr-codes/destination" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "제주도",
    "useful_links": {
      "tourism_board": "https://www.visitjeju.net",
      "hotels": ["https://agoda.com/jeju"],
      "restaurants": ["https://naver.me/jeju"]
    }
  }'
```

**응답:**
```json
{
  "destination": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=%EC%A0%9C%EC%A3%BC%EB%8F%84",
  "tourism_board": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fwww.visitjeju.net",
  "hotels": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fagoda.com%2Fjeju",
  "restaurants": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fnaver.me%2Fjeju"
}
```

---

### 5️⃣ 앱 다운로드 QR 코드

**요청:**
```bash
curl -X POST "http://localhost:8000/api/v1/qr-codes/app-download" \
  -H "Content-Type: application/json" \
  -d '{
    "ios": "https://apps.apple.com/kr/app/travel-planner/id1234567890",
    "android": "https://play.google.com/store/apps/details?id=com.travel.planner"
  }'
```

**응답:**
```json
{
  "ios": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fapps.apple.com%2F...",
  "android": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fplay.google.com%2F..."
}
```

---

### 6️⃣ WiFi 연결 QR 코드

**요청:**
```bash
# 기본 WPA WiFi
curl -X GET "http://localhost:8000/api/v1/qr-codes/wifi?ssid=Hotel-WiFi&password=password123&security=WPA"

# 숨겨진 네트워크
curl -X GET "http://localhost:8000/api/v1/qr-codes/wifi?ssid=Hidden-Network&password=secret&security=WPA&hidden=true"

# 보안 없음
curl -X GET "http://localhost:8000/api/v1/qr-codes/wifi?ssid=Free-WiFi&password=&security=nopass"
```

**쿼리 파라미터:**
- `ssid`: WiFi 네트워크명 (필수)
- `password`: WiFi 비밀번호 (필수, 없으면 빈 문자열)
- `security`: 보안 타입 (WPA/WEP/nopass, 기본값: WPA)
- `hidden`: 숨겨진 네트워크 (true/false)

**응답:**
```json
{
  "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=WIFI%3AT%3AWPA%3BS%3AHotel-WiFi%3BP%3Apassword123%3BH%3Afalse%3B%3B",
  "ssid": "Hotel-WiFi",
  "security": "WPA",
  "hidden": false
}
```

**스마트폰 사용:**
- iOS: 카메라 앱에서 QR 코드 스캔 → WiFi 연결 팝업
- Android: Google Lens 또는 WiFi QR 코드 앱으로 스캔

---

### 7️⃣ 연락처(vCard) QR 코드

**요청:**
```bash
# 기본 연락처
curl -X GET "http://localhost:8000/api/v1/qr-codes/contact?name=김여행&phone=010-1234-5678&email=travel@example.com"

# 조직 포함
curl -X GET "http://localhost:8000/api/v1/qr-codes/contact?name=김여행&phone=010-1234-5678&email=travel@example.com&organization=여행사"
```

**쿼리 파라미터:**
- `name`: 이름 (필수)
- `phone`: 전화번호 (선택)
- `email`: 이메일 (선택)
- `organization`: 조직명 (선택)

**응답:**
```json
{
  "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=BEGIN%3AVCARD%0AVERSION%3A3.0%0AFN%3A%EC%97%AC%ED%96%89...",
  "name": "김여행",
  "phone": "010-1234-5678",
  "email": "travel@example.com",
  "organization": "여행사"
}
```

---

### 8️⃣ 지원 포맷 확인

**요청:**
```bash
curl -X GET "http://localhost:8000/api/v1/qr-codes/formats"
```

**응답:**
```json
{
  "formats": ["png", "jpg", "svg", "webp"],
  "descriptions": {
    "png": "PNG 이미지 (권장, 배경 투명)",
    "jpg": "JPEG 이미지 (용량 작음)",
    "svg": "벡터 형식 (확대/축소 무손실)",
    "webp": "최신 포맷 (가장 작은 용량)"
  },
  "recommended": "svg (인쇄용) / png (웹용)"
}
```

---

### 9️⃣ API 정보 조회

**요청:**
```bash
curl -X GET "http://localhost:8000/api/v1/qr-codes/info"
```

**응답:**
```json
{
  "title": "QR Code Generator API",
  "description": "다양한 정보를 QR 코드로 변환하는 API",
  "max_data_length": 4296,
  "min_size": 50,
  "max_size": 1000,
  "supported_formats": ["png", "jpg", "svg", "webp"],
  "use_cases": [
    "여행지 정보 및 예약 링크",
    "교통편 정보 및 발권 링크",
    "호텔/숙박 예약 링크",
    "WiFi 자동 연결",
    "연락처 공유",
    "앱 다운로드 링크"
  ],
  "tips": [
    "큰 크기(400x400 이상) 권장 - 스캔 거리 증가",
    "SVG 형식은 벡터이므로 해상도 무관",
    "PNG는 투명 배경으로 웹 통합 용이",
    "실시간 생성되므로 캐싱 고려"
  ]
}
```

---

## 📊 포맷 비교

| 포맷 | 용도 | 장점 | 단점 |
|------|------|------|------|
| PNG | 웹, 이메일 | 투명 배경, 품질 좋음 | 용량 중간 |
| JPG | 사진, 문서 | 용량 작음 | 배경 흰색만 가능 |
| SVG | 인쇄, 확대 | 해상도 무관, 벡터 | 복잡한 데이터 |
| WebP | 최신 웹 | 가장 작은 용량 | 지원율 낮음 |

**권장:**
- 웹: PNG (200x200)
- 인쇄: SVG (300x300)
- 모바일: WebP (150x150)

---

## 🔐 보안 고려사항

1. **URL 인코딩**: 특수문자 자동 처리 (안전함)
2. **데이터 길이**: 최대 4296자
3. **외부 API**: QR Server (신뢰할 수 있는 서비스)
4. **프라이버시**: 생성된 QR 코드는 외부 서버에 저장되지 않음

---

## 💡 실사용 예시

### 여행 패키지 QR 코드

```json
{
  "name": "제주도 3박 4일 패키지",
  "useful_links": {
    "booking": "https://travelapp.com/package/123",
    "insurance": "https://insurance.com/travel",
    "guide": "https://guide.travelapp.com/jeju"
  }
}
```

### 교통편 티켓 QR 코드

```json
{
  "provider": "Korean Air",
  "departure_city": "서울",
  "arrival_city": "제주",
  "booking_methods": [
    {
      "platform": "Check-in",
      "url": "https://checkin.koreanair.com/booking123"
    }
  ]
}
```

### 호텔 WiFi 공유

호텔 프론트에서 게스트들에게 QR 코드 제공:
```
https://localhost:8000/api/v1/qr-codes/wifi?ssid=Jeju-Hotel&password=guest2024
```

---

## ✅ 테스트 체크리스트

- [ ] 기본 QR 코드 생성 (200)
- [ ] 다양한 포맷 지원 (png/jpg/svg/webp)
- [ ] 예약 링크 QR 코드 (200)
- [ ] 교통편 정보 QR 코드 (200)
- [ ] 여행지 정보 QR 코드 (200)
- [ ] 앱 다운로드 QR 코드 (200)
- [ ] WiFi QR 코드 생성 (200)
- [ ] 연락처 QR 코드 생성 (200)
- [ ] 포맷 정보 조회 (200)
- [ ] API 정보 조회 (200)
- [ ] 크기 범위 검증 (50-1000)
- [ ] 필수 파라미터 검증 (400)

---

## 🔄 다음 단계

- Task #9: 프론트엔드 페이지 완성 (search.html, create-itinerary.html, etc.)
- Task #10: 전체 시스템 통합 테스트

---

## 📝 참고

**외부 API 사용:**
- QR Server: https://qr-server.com/
- 무료이며 가입 불필요
- 높은 가용성과 속도
- 실시간 생성으로 항상 최신 데이터

**성능 최적화:**
- QR 코드 URL을 캐싱하여 재사용 권장
- 클라이언트에서 img src로 직접 호출 가능
- 일괄 요청 시 Promise.all() 사용 권장

**축하합니다! QR 코드 생성 API가 완성되었습니다!** 📱✨
