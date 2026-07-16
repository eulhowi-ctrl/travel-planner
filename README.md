# 🌍 TRAVEL - AI 여행 플래너

여행지 탐색부터 일정 생성, 예산 관리까지 지원하는 정적(static) 웹 애플리케이션입니다.

[English](#english) | [한국어](#korean)

---

## 한국어 <a name="korean"></a>

### 📋 개요

TRAVEL은 백엔드 서버 없이 브라우저(LocalStorage)만으로 동작하는 여행 계획 앱입니다. 코드는 전부 `travel/` 폴더 안에 있으며, HTML/CSS/바닐라 JS 외에 별도 빌드 과정이 없습니다.

**주요 기능:**
- 🔍 35개국 423개 여행지 검색 (키워드/국가/테마/활동/가격/기간/계절 필터)
- 🗺️ Leaflet 기반 실제 지도 + 가격 표시 마커
- 📅 여행 일정 관리 및 위시리스트 → 자동 일정 생성
- 🌤️ 실시간 날씨 (OpenWeather API, 키 없으면 데모 데이터로 자동 전환)
- 💰 예산 관리 + 실시간 환율 변환 (API 실패 시 캐시된 값으로 폴백)
- 🚗 도시별 장거리/지역 교통 정보 및 현지인 팁
- 🎫 예약 확인 / WiFi / 연락처 QR 코드 생성
- 💬 커뮤니티 (Q&A, 여행기, 여행버디, 베스트리뷰어)
- 🏅 포인트/리워드, AI 챗봇, 호스트 프로필, 패키지 상품

### 🚀 빠른 시작

빌드나 서버 설치 없이 정적 파일만 서빙하면 됩니다.

```bash
# 1. 저장소 클론
git clone https://github.com/eulhowi-ctrl/travel-planner.git
cd travel-planner/travel

# 2. 정적 서버 실행 (택1)
python -m http.server 8000
# 또는: npx serve .

# 3. 브라우저에서 접속
# http://localhost:8000/index.html
```

`travel/index.html`을 브라우저로 직접 열어도 대부분 기능은 동작하지만, 날씨/환율 API 호출은 `http://` 또는 `https://` 오리진에서 실행하는 것을 권장합니다.

### 🏗️ 기술 스택

- **Vanilla HTML5 / CSS3 / JavaScript (ES6+)** — 프레임워크·빌드 도구 없음
- **LocalStorage** — 위시리스트, 포인트, 예약, 예산, 사용자 프로필 등 모든 상태 저장
- **Leaflet.js** (CDN) — 여행지 지도
- **OpenWeather API** — 실시간 날씨 (`travel/weather-api.js`)
- **환율 API** (er-api.com 등, 캐시 폴백 포함) — 예산 페이지 통화 변환 (`travel/exchange-api.js`)
- **QR Server API** (api.qrserver.com) — QR 코드 생성 (`travel/qr-generator.js`)

### 📁 주요 파일

| 파일 | 역할 |
|---|---|
| `travel/index.html` ~ `travel/chatbot.html` | 12개 페이지 (홈/검색/일정/갤러리/위시리스트/예산/예약/패키지/커뮤니티/호스트/포인트/챗봇) |
| `travel/script.js` | 공통 헤더/푸터 렌더링, 공유 헬퍼 |
| `travel/destinations-data.js` | 여행지 데이터셋 (35개국 423곳) |
| `travel/community-script.js` | 커뮤니티 탭 렌더링 |

### 📖 배포

정적 파일이므로 GitHub Pages, Netlify, Vercel 등 어떤 정적 호스팅에도 `travel/` 폴더를 그대로 배포하면 됩니다. 서버/DB/Docker가 필요 없습니다.

---

## English <a name="english"></a>

### 📋 Overview

TRAVEL is a client-only travel planning app — no backend, all state lives in LocalStorage. Everything lives under `travel/`: plain HTML/CSS/vanilla JS, no build step.

**Key Features:**
- 🔍 Search across 423 destinations in 35 countries (keyword/country/theme/activity/price/duration/season filters)
- 🗺️ Real Leaflet map with price-bubble markers
- 📅 Itinerary management + auto-generated itinerary from your wishlist
- 🌤️ Live weather via OpenWeather API (falls back to demo data if no key is set)
- 💰 Budget tracking with live currency conversion (cache fallback if the API is unavailable)
- 🚗 Per-city transportation info and local tips
- 🎫 QR codes for booking confirmations, WiFi, and contact info
- 💬 Community hub (Q&A, trip reports, travel buddies, top reviewers)
- 🏅 Points/rewards, AI chatbot, host profiles, travel packages

### 🚀 Quick Start

No build tools or server framework required — just serve the static files.

```bash
# 1. Clone the repository
git clone https://github.com/eulhowi-ctrl/travel-planner.git
cd travel-planner/travel

# 2. Run a static server (pick one)
python -m http.server 8000
# or: npx serve .

# 3. Open in your browser
# http://localhost:8000/index.html
```

Opening `travel/index.html` directly from disk mostly works too, but serving over `http(s)://` is recommended so the weather/exchange-rate API calls behave correctly.

### 🏗️ Tech Stack

- **Vanilla HTML5 / CSS3 / JavaScript (ES6+)** — no framework, no build tooling
- **LocalStorage** — wishlist, points, bookings, budget items, user profile, etc.
- **Leaflet.js** (CDN) — destination map
- **OpenWeather API** — live weather (`travel/weather-api.js`)
- **Exchange rate API** (e.g. er-api.com, with cache fallback) — currency conversion on the budget page (`travel/exchange-api.js`)
- **QR Server API** (api.qrserver.com) — QR code generation (`travel/qr-generator.js`)

### 📁 Key Files

| File | Purpose |
|---|---|
| `travel/index.html` – `travel/chatbot.html` | 12 pages (home/search/itinerary/gallery/wishlist/budget/booking/packages/community/host/rewards/chatbot) |
| `travel/script.js` | Shared header/footer rendering and helpers |
| `travel/destinations-data.js` | Destination dataset (423 places across 35 countries) |
| `travel/community-script.js` | Community tab rendering |

### 📖 Deployment

Since it's fully static, deploy the `travel/` folder as-is to any static host (GitHub Pages, Netlify, Vercel, ...). No server, database, or Docker required.

---

**Created with ❤️ for travel enthusiasts**
