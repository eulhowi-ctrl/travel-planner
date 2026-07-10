from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


# ==================== Enums ====================
class TravelThemeEnum(str, Enum):
    COUPLE = "couple"
    FAMILY = "family"
    SOLO = "solo"
    FRIENDS = "friends"


class BudgetLevelEnum(str, Enum):
    BUDGET = "budget"
    STANDARD = "standard"
    LUXURY = "luxury"


class TransportTypeEnum(str, Enum):
    FLIGHT = "flight"
    TRAIN = "train"
    BUS = "bus"
    CAR = "car"


class LocalTransportTypeEnum(str, Enum):
    BUS = "bus"
    SUBWAY = "subway"
    TAXI = "taxi"
    RENTAL_CAR = "rental_car"


# ==================== User Schemas ====================
class UserBase(BaseModel):
    email: EmailStr
    username: str


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== User Profile Schemas ====================
class UserProfileBase(BaseModel):
    travel_theme: TravelThemeEnum
    family_size: Optional[int] = None
    has_children: bool = False
    children_ages: Optional[List[int]] = None
    preferred_activities: Optional[List[str]] = None
    budget_level: BudgetLevelEnum


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(BaseModel):
    travel_theme: Optional[TravelThemeEnum] = None
    family_size: Optional[int] = None
    has_children: Optional[bool] = None
    children_ages: Optional[List[int]] = None
    preferred_activities: Optional[List[str]] = None
    budget_level: Optional[BudgetLevelEnum] = None


class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class UserFullResponse(UserResponse):
    profile: Optional[UserProfileResponse] = None


# ==================== Destination Schemas ====================
class DestinationBase(BaseModel):
    name: str
    location: str
    country: str
    description: str
    themes: List[str] = []
    suitable_for_children: bool = False
    activities: List[str] = []


class DestinationCreate(DestinationBase):
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    family_size_recommended: Optional[Dict[str, int]] = None
    useful_links: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None


class DestinationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    themes: Optional[List[str]] = None
    suitable_for_children: Optional[bool] = None
    activities: Optional[List[str]] = None
    useful_links: Optional[Dict[str, Any]] = None


class DestinationResponse(DestinationBase):
    id: int
    latitude: Optional[float]
    longitude: Optional[float]
    family_size_recommended: Optional[Dict[str, int]]
    useful_links: Optional[Dict[str, Any]]
    images: List[str]
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Long Distance Transportation Schemas ====================
class BookingMethod(BaseModel):
    platform: str
    url: str
    how_to: str


class LongDistanceTransportationBase(BaseModel):
    type: TransportTypeEnum
    departure_city: str
    arrival_city: str
    departure_time: datetime
    arrival_time: datetime
    price: float
    currency: str = "KRW"
    provider: str


class LongDistanceTransportationCreate(LongDistanceTransportationBase):
    duration_minutes: Optional[int] = None
    provider_code: Optional[str] = None
    booking_methods: Optional[List[BookingMethod]] = None
    directions: Optional[str] = None
    booking_qr_links: Optional[Dict[str, Any]] = None


class LongDistanceTransportationResponse(LongDistanceTransportationBase):
    id: int
    duration_minutes: int
    provider_code: Optional[str]
    booking_methods: Optional[List[BookingMethod]]
    directions: Optional[str]
    booking_qr_links: Optional[Dict[str, Any]]
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Local Transportation Schemas ====================
class LocalTransportationBase(BaseModel):
    transport_type: LocalTransportTypeEnum
    city: str
    fare: float
    currency: str = "KRW"
    operating_hours: Dict[str, str]


class LocalTransportationCreate(LocalTransportationBase):
    destination_id: int
    route_number: Optional[str] = None
    route_details: Optional[List[str]] = None
    frequency: Optional[str] = None
    payment_methods: Optional[List[str]] = None
    card_types: Optional[List[str]] = None
    base_fare: Optional[float] = None
    distance_per_km: Optional[float] = None
    time_unit_fare: Optional[float] = None
    calling_apps: Optional[List[str]] = None
    tip_culture: Optional[str] = None
    app_download_links: Optional[Dict[str, str]] = None
    useful_links: Optional[Dict[str, str]] = None
    directions: Optional[str] = None


class LocalTransportationResponse(LocalTransportationBase):
    id: int
    destination_id: int
    route_number: Optional[str]
    route_details: Optional[List[str]]
    frequency: Optional[str]
    payment_methods: Optional[List[str]]
    card_types: Optional[List[str]]
    base_fare: Optional[float]
    calling_apps: Optional[List[str]]
    tip_culture: Optional[str]
    app_download_links: Optional[Dict[str, str]]
    useful_links: Optional[Dict[str, str]]
    directions: Optional[str]

    class Config:
        from_attributes = True


# ==================== Budget Schemas ====================
class BudgetBase(BaseModel):
    category: str  # flight, accommodation, meal, activity, transport
    item_name: str
    estimated_cost: float
    currency: str = "KRW"


class BudgetCreate(BudgetBase):
    actual_cost: Optional[float] = None
    notes: Optional[str] = None


class BudgetUpdate(BaseModel):
    item_name: Optional[str] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    notes: Optional[str] = None


class BudgetResponse(BudgetBase):
    id: int
    itinerary_id: int
    actual_cost: Optional[float]
    notes: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class BudgetSummary(BaseModel):
    total_estimated: float
    total_actual: Optional[float]
    remaining_budget: Optional[float]
    by_category: Dict[str, Dict[str, float]]


# ==================== Itinerary Schemas ====================
class ActivityItem(BaseModel):
    time: str  # "10:00"
    place: str
    duration: int  # minutes
    notes: Optional[str] = None


class ItineraryDayBase(BaseModel):
    day_number: int
    destination_id: int
    date: datetime
    activities: Optional[List[ActivityItem]] = []


class ItineraryDayCreate(ItineraryDayBase):
    arrival_transport_id: Optional[int] = None
    departure_transport_id: Optional[int] = None
    notes: Optional[str] = None


class ItineraryDayResponse(ItineraryDayCreate):
    id: int
    itinerary_id: int

    class Config:
        from_attributes = True


class ItineraryBase(BaseModel):
    title: str
    departure_city: str
    start_date: datetime
    end_date: datetime
    travel_theme: TravelThemeEnum


class ItineraryCreate(ItineraryBase):
    description: Optional[str] = None
    budget_allocated: Optional[float] = None


class ItineraryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    budget_allocated: Optional[float] = None
    is_active: Optional[bool] = None


class ItineraryResponse(ItineraryBase):
    id: int
    user_id: int
    description: Optional[str]
    budget_allocated: Optional[float]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ItineraryDetailResponse(ItineraryResponse):
    itinerary_days: List[ItineraryDayResponse]
    budgets: List[BudgetResponse]


# ==================== QR Code Schemas ====================
class QRCodeResponse(BaseModel):
    id: int
    original_url: str
    qr_code_path: str
    label: str
    category: str
    created_at: datetime

    class Config:
        from_attributes = True


# ==================== Auth Schemas ====================
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None
