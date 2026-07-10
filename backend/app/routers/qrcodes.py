from fastapi import APIRouter, Query, HTTPException, status
from typing import Optional, Dict
from urllib.parse import quote

from app.utils.qr_generator import (
    generate_qr_code_url,
    create_booking_qr_links,
    create_transport_qr_links,
    create_destination_qr_links,
    create_app_download_qr_links,
    generate_wifi_qr,
    generate_vcard_qr,
)

router = APIRouter()


# ==================== QR Code Generation ====================

@router.get("/generate", response_model=Dict[str, str])
async def generate_qr_code(
    data: str = Query(..., description="QR 코드로 변환할 데이터 (URL 등)"),
    size: int = Query(200, ge=50, le=1000, description="QR 코드 크기 (50-1000)"),
    format_type: str = Query("png", regex="^(png|jpg|svg|webp)$", description="포맷 (png/jpg/svg/webp)")
):
    """
    기본 QR 코드 생성

    **사용 예시:**
    - URL: `data=https://www.koreanair.com`
    - 텍스트: `data=제주도 여행`
    - 전화번호: `data=tel:+82-2-123-4567`

    **응답:**
    ```json
    {
      "qr_code_url": "https://api.qrserver.com/v1/create-qr-code/?...",
      "data": "https://www.koreanair.com",
      "size": 200,
      "format": "png"
    }
    ```
    """
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="데이터를 입력하세요."
        )

    qr_url = generate_qr_code_url(data, size, format_type)

    return {
        "qr_code_url": qr_url,
        "data": data,
        "size": str(size),
        "format": format_type
    }


@router.post("/booking", response_model=Dict)
async def generate_booking_qr_codes(
    booking_data: Dict
):
    """
    예약 링크 QR 코드 생성

    **요청 본문:**
    ```json
    {
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
    }
    ```

    **응답:**
    ```json
    {
      "qr_codes": {
        "official_website": "https://...",
        "naver_travel": "https://..."
      }
    }
    ```
    """
    if "booking_methods" not in booking_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="booking_methods가 필요합니다."
        )

    qr_links = create_booking_qr_links(booking_data["booking_methods"])

    return {
        "qr_codes": qr_links,
        "total_codes": len(qr_links)
    }


@router.post("/transportation", response_model=Dict)
async def generate_transportation_qr_codes(
    transport_data: Dict
):
    """
    교통편 정보 QR 코드 생성

    **요청 본문:**
    ```json
    {
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
    }
    ```

    **응답:**
    ```json
    {
      "route_info": "https://...",
      "booking_links": {
        "official_website": "https://..."
      }
    }
    ```
    """
    if not transport_data.get("departure_city") or not transport_data.get("arrival_city"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="departure_city와 arrival_city가 필요합니다."
        )

    qr_codes = create_transport_qr_links(transport_data)

    return qr_codes


@router.post("/destination", response_model=Dict)
async def generate_destination_qr_codes(
    destination_data: Dict
):
    """
    여행지 정보 QR 코드 생성

    **요청 본문:**
    ```json
    {
      "name": "제주도",
      "useful_links": {
        "tourism_board": "https://www.visitjeju.net",
        "hotels": ["https://agoda.com/jeju"],
        "restaurants": ["https://naver.me/jeju"]
      }
    }
    ```

    **응답:**
    ```json
    {
      "destination": "https://...",
      "tourism_board": "https://...",
      "hotels": "https://..."
    }
    ```
    """
    if "name" not in destination_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="destination name이 필요합니다."
        )

    qr_codes = create_destination_qr_links(destination_data)

    return qr_codes


@router.post("/app-download", response_model=Dict)
async def generate_app_download_qr_codes(
    app_data: Dict
):
    """
    앱 다운로드 QR 코드 생성

    **요청 본문:**
    ```json
    {
      "ios": "https://apps.apple.com/app/...",
      "android": "https://play.google.com/store/apps/..."
    }
    ```

    **응답:**
    ```json
    {
      "ios": "https://...",
      "android": "https://..."
    }
    ```
    """
    if not app_data.get("ios") and not app_data.get("android"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ios 또는 android 링크가 필요합니다."
        )

    qr_codes = create_app_download_qr_links(app_data)

    return qr_codes


@router.get("/wifi", response_model=Dict)
async def generate_wifi_qr_code(
    ssid: str = Query(..., description="WiFi 네트워크명"),
    password: str = Query(..., description="WiFi 비밀번호"),
    security: str = Query("WPA", regex="^(WPA|WEP|nopass)$", description="보안 타입"),
    hidden: bool = Query(False, description="숨겨진 네트워크 여부")
):
    """
    WiFi 연결 QR 코드 생성

    스마트폰으로 QR 코드를 스캔하면 자동으로 WiFi에 연결됩니다.

    **요청 예시:**
    ```
    /api/v1/qr-codes/wifi?ssid=Hotel-WiFi&password=password123&security=WPA
    ```

    **응답:**
    ```json
    {
      "qr_code_url": "https://...",
      "ssid": "Hotel-WiFi",
      "security": "WPA"
    }
    ```
    """
    qr_url = generate_wifi_qr(ssid, password, security, hidden)

    return {
        "qr_code_url": qr_url,
        "ssid": ssid,
        "security": security,
        "hidden": hidden
    }


@router.get("/contact", response_model=Dict)
async def generate_contact_qr_code(
    name: str = Query(..., description="이름"),
    phone: str = Query(None, description="전화번호"),
    email: str = Query(None, description="이메일"),
    organization: str = Query(None, description="조직명")
):
    """
    연락처(vCard) QR 코드 생성

    스마트폰으로 스캔하면 연락처를 추가할 수 있습니다.

    **요청 예시:**
    ```
    /api/v1/qr-codes/contact?name=김여행&phone=010-1234-5678&email=travel@example.com&organization=여행사
    ```

    **응답:**
    ```json
    {
      "qr_code_url": "https://...",
      "name": "김여행",
      "phone": "010-1234-5678",
      "email": "travel@example.com"
    }
    ```
    """
    qr_url = generate_vcard_qr(name, phone, email, organization)

    return {
        "qr_code_url": qr_url,
        "name": name,
        "phone": phone or "N/A",
        "email": email or "N/A",
        "organization": organization or "N/A"
    }


# ==================== QR Code Information ====================

@router.get("/formats", response_model=Dict)
async def get_qr_code_formats():
    """
    지원하는 QR 코드 포맷 목록

    **응답:**
    ```json
    {
      "formats": ["png", "jpg", "svg", "webp"],
      "descriptions": {...}
    }
    ```
    """
    return {
        "formats": ["png", "jpg", "svg", "webp"],
        "descriptions": {
            "png": "PNG 이미지 (권장, 배경 투명)",
            "jpg": "JPEG 이미지 (용량 작음)",
            "svg": "벡터 형식 (확대/축소 무손실)",
            "webp": "최신 포맷 (가장 작은 용량)"
        },
        "recommended": "svg (인쇄용) / png (웹용)"
    }


@router.get("/info", response_model=Dict)
async def get_qr_code_info():
    """
    QR 코드 생성 API 정보 및 사용 팁

    **응답:**
    ```json
    {
      "max_data_length": 4296,
      "min_size": 50,
      "max_size": 1000,
      "use_cases": [...]
    }
    ```
    """
    return {
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
