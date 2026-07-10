"""
QR 코드 생성 유틸리티
외부 API를 사용하여 QR 코드 생성 (의존성 최소화)
"""

from urllib.parse import quote
from typing import Optional, Dict, List

# QR 코드 생성 서비스 URL (의존성 불필요)
# QR Server: https://qr-server.com/ (무료, 외부 호스팅)
QR_SERVER_URL = "https://api.qrserver.com/v1/create-qr-code/"


def generate_qr_code_url(
    data: str,
    size: int = 200,
    format_type: str = "png"
) -> str:
    """
    외부 API를 사용하여 QR 코드 URL 생성

    Args:
        data: QR 코드로 변환할 데이터 (URL, 텍스트 등)
        size: QR 코드 크기 (기본값: 200x200)
        format_type: 포맷 (png, jpg, svg, webp)

    Returns:
        QR 코드 이미지 URL

    Example:
        >>> url = generate_qr_code_url("https://www.koreanair.com")
        >>> print(url)
        https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=https%3A%2F%2Fwww.koreanair.com
    """
    if format_type == "svg":
        # SVG 형식
        return f"{QR_SERVER_URL}?format=svg&data={quote(data)}"
    else:
        # 기본 형식 (PNG, JPG, WEBP)
        return f"{QR_SERVER_URL}?size={size}x{size}&format={format_type}&data={quote(data)}"


def generate_qr_code_html(data: str, size: int = 200, alt_text: str = "QR Code") -> str:
    """
    HTML img 태그로 QR 코드 반환

    Args:
        data: QR 코드로 변환할 데이터
        size: QR 코드 크기
        alt_text: 이미지 alt 텍스트

    Returns:
        HTML img 태그

    Example:
        >>> html = generate_qr_code_html("https://www.koreanair.com", alt_text="Korean Air")
        >>> print(html)
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200..." alt="Korean Air" />
    """
    qr_url = generate_qr_code_url(data, size)
    return f'<img src="{qr_url}" alt="{alt_text}" width="{size}" height="{size}" />'


def create_booking_qr_links(booking_methods: List[Dict]) -> Dict[str, str]:
    """
    예약 방법별 QR 코드 링크 생성

    Args:
        booking_methods: 예약 방법 리스트
            [
                {
                    "platform": "Official Website",
                    "url": "https://...",
                    "how_to": "Direct booking"
                }
            ]

    Returns:
        {"platform": qr_url, ...}

    Example:
        >>> booking = [
        ...     {"platform": "Official Website", "url": "https://www.koreanair.com"},
        ...     {"platform": "Naver Travel", "url": "https://travel.naver.com"}
        ... ]
        >>> links = create_booking_qr_links(booking)
        >>> print(links["official_website"])
        https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=...
    """
    qr_links = {}

    for method in booking_methods:
        if "url" in method and method["url"]:
            platform = method.get("platform", "booking").lower()
            platform = platform.replace(" ", "_").replace("/", "_")
            qr_links[platform] = generate_qr_code_url(method["url"])

    return qr_links


def create_transport_qr_links(transport_data: Dict) -> Dict:
    """
    교통편 정보용 QR 코드 링크 생성

    Args:
        transport_data: 교통편 정보
            {
                "provider": "Korean Air",
                "departure_city": "서울",
                "arrival_city": "제주",
                "booking_methods": [...],
                "booking_qr_links": {...}  # 기존 링크가 있으면 유지
            }

    Returns:
        QR 코드 링크 딕셔너리
        {
            "route_info": "https://...",
            "booking_links": {...}
        }

    Example:
        >>> transport = {
        ...     "provider": "Korean Air",
        ...     "departure_city": "서울",
        ...     "arrival_city": "제주",
        ...     "booking_methods": [{"platform": "...", "url": "..."}]
        ... }
        >>> links = create_transport_qr_links(transport)
    """
    qr_info = {}

    # 여행 경로 정보
    departure = transport_data.get("departure_city", "")
    arrival = transport_data.get("arrival_city", "")
    if departure and arrival:
        route_text = f"{departure} → {arrival}"
        qr_info["route_info"] = generate_qr_code_url(route_text)

    # 예약 링크
    if "booking_methods" in transport_data:
        booking_qr = create_booking_qr_links(transport_data["booking_methods"])
        if booking_qr:
            qr_info["booking_links"] = booking_qr

    return qr_info


def create_destination_qr_links(destination_data: Dict) -> Dict[str, str]:
    """
    여행지 정보용 QR 코드 링크 생성

    Args:
        destination_data: 여행지 정보
            {
                "name": "제주도",
                "useful_links": {
                    "tourism_board": "https://...",
                    "hotels": ["https://..."]
                }
            }

    Returns:
        QR 코드 링크 딕셔너리
        {
            "destination": "https://...",
            "tourism_board": "https://...",
            "hotels": "https://..."
        }
    """
    qr_links = {}

    # 목적지 정보
    if "name" in destination_data:
        qr_links["destination"] = generate_qr_code_url(destination_data["name"])

    # 유용한 링크들
    if "useful_links" in destination_data:
        useful_links = destination_data["useful_links"]

        if isinstance(useful_links, dict):
            for link_name, link_value in useful_links.items():
                # 링크 목록인 경우 첫 번째만 사용
                if isinstance(link_value, list):
                    link_value = link_value[0] if link_value else None

                if link_value:
                    qr_links[link_name] = generate_qr_code_url(link_value)

    return qr_links


def create_app_download_qr_links(app_data: Dict) -> Dict[str, str]:
    """
    모바일 앱 다운로드 링크용 QR 코드 생성

    Args:
        app_data: 앱 정보
            {"ios": "https://apps.apple.com/...", "android": "https://play.google.com/..."}

    Returns:
        {"ios": qr_url, "android": qr_url}

    Example:
        >>> apps = {
        ...     "ios": "https://apps.apple.com/app/...",
        ...     "android": "https://play.google.com/store/apps/..."
        ... }
        >>> qr = create_app_download_qr_links(apps)
    """
    qr_links = {}

    if "ios" in app_data and app_data["ios"]:
        qr_links["ios"] = generate_qr_code_url(app_data["ios"])

    if "android" in app_data and app_data["android"]:
        qr_links["android"] = generate_qr_code_url(app_data["android"])

    return qr_links


def create_payment_card_qr_links(card_info: Dict) -> Dict[str, str]:
    """
    교통카드/결제카드 정보용 QR 코드

    Args:
        card_info: 카드 정보
            {"name": "T-money", "website": "https://...", "app_link": "..."}

    Returns:
        {"card_website": qr_url, "app_download": qr_url}
    """
    qr_links = {}

    if "website" in card_info and card_info["website"]:
        qr_links["card_website"] = generate_qr_code_url(card_info["website"])

    if "app_link" in card_info and card_info["app_link"]:
        qr_links["app_download"] = generate_qr_code_url(card_info["app_link"])

    return qr_links


def generate_vcard_qr(
    name: str,
    phone: Optional[str] = None,
    email: Optional[str] = None,
    organization: Optional[str] = None
) -> str:
    """
    연락처(vCard) QR 코드 생성

    Args:
        name: 이름
        phone: 전화번호
        email: 이메일
        organization: 조직명

    Returns:
        vCard QR 코드 URL
    """
    vcard_data = f"BEGIN:VCARD\nVERSION:3.0\nFN:{name}\n"

    if phone:
        vcard_data += f"TEL:{phone}\n"
    if email:
        vcard_data += f"EMAIL:{email}\n"
    if organization:
        vcard_data += f"ORG:{organization}\n"

    vcard_data += "END:VCARD"

    return generate_qr_code_url(vcard_data)


def generate_wifi_qr(
    ssid: str,
    password: str,
    security: str = "WPA",
    hidden: bool = False
) -> str:
    """
    WiFi 연결 QR 코드 생성

    Args:
        ssid: WiFi 네트워크명
        password: WiFi 비밀번호
        security: 보안 타입 (WPA, WEP, nopass)
        hidden: 숨겨진 네트워크 여부

    Returns:
        WiFi QR 코드 URL
    """
    hidden_str = "true" if hidden else "false"
    wifi_string = f"WIFI:T:{security};S:{ssid};P:{password};H:{hidden_str};;"

    return generate_qr_code_url(wifi_string)


if __name__ == "__main__":
    # 테스트
    print("=" * 60)
    print("QR Code Generator Test")
    print("=" * 60)

    # 1. 기본 URL QR 코드
    test_url = "https://www.koreanair.com"
    print(f"\n1️⃣ URL QR Code:")
    print(f"   Input: {test_url}")
    print(f"   QR Code: {generate_qr_code_url(test_url)}")

    # 2. 예약 QR 링크
    test_booking = [
        {"platform": "Official Website", "url": "https://www.koreanair.com"},
        {"platform": "Naver Travel", "url": "https://travel.naver.com"}
    ]
    print(f"\n2️⃣ Booking QR Links:")
    booking_qr = create_booking_qr_links(test_booking)
    for platform, qr_url in booking_qr.items():
        print(f"   {platform}: {qr_url[:80]}...")

    # 3. 교통편 QR 링크
    test_transport = {
        "provider": "Korean Air",
        "departure_city": "서울",
        "arrival_city": "제주",
        "booking_methods": test_booking
    }
    print(f"\n3️⃣ Transport QR Links:")
    transport_qr = create_transport_qr_links(test_transport)
    for key, value in transport_qr.items():
        if isinstance(value, dict):
            print(f"   {key}: {len(value)} links")
        else:
            print(f"   {key}: {str(value)[:80]}...")

    # 4. WiFi QR
    print(f"\n4️⃣ WiFi QR Code:")
    wifi_qr = generate_wifi_qr("Jeju-Hotel-WiFi", "password123")
    print(f"   {wifi_qr[:80]}...")

    print("\n✅ All QR codes generated successfully!")
