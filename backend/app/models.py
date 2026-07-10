from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, Text, JSON, ForeignKey, Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()


# ==================== Enums ====================
class TravelTheme(str, enum.Enum):
    COUPLE = "couple"
    FAMILY = "family"
    SOLO = "solo"
    FRIENDS = "friends"


class BudgetLevel(str, enum.Enum):
    BUDGET = "budget"
    STANDARD = "standard"
    LUXURY = "luxury"


class TransportType(str, enum.Enum):
    FLIGHT = "flight"
    TRAIN = "train"
    BUS = "bus"
    CAR = "car"


class LocalTransportType(str, enum.Enum):
    BUS = "bus"
    SUBWAY = "subway"
    TAXI = "taxi"
    RENTAL_CAR = "rental_car"


# ==================== Users & Profiles ====================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    itineraries = relationship("Itinerary", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)

    # Travel Preferences
    travel_theme = Column(SQLEnum(TravelTheme), default=TravelTheme.FAMILY)
    family_size = Column(Integer, nullable=True)  # 가족 인원수
    has_children = Column(Boolean, default=False)
    children_ages = Column(JSON, nullable=True)  # [3, 8, 12]
    preferred_activities = Column(JSON, default=[])  # ["hiking", "beach", "culture"]
    budget_level = Column(SQLEnum(BudgetLevel), default=BudgetLevel.STANDARD)

    # Relationships
    user = relationship("User", back_populates="profile")


# ==================== Destinations ====================
class Destination(Base):
    __tablename__ = "destinations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)  # 국가/지역
    country = Column(String)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    description = Column(Text)

    # Theme & Tags
    themes = Column(JSON, default=[])  # ["couple", "family", "kids-friendly"]
    suitable_for_children = Column(Boolean, default=False)
    family_size_recommended = Column(JSON, nullable=True)  # {min: 2, max: 10}
    activities = Column(JSON, default=[])  # ["hiking", "museum", "beach"]

    # Links & QR Codes
    useful_links = Column(JSON, nullable=True)  # {
    #   "tourism_board": "https://...",
    #   "hotels": ["https://..."],
    #   "restaurants": ["https://..."]
    # }

    # Media
    images = Column(JSON, default=[])  # URLs

    # Metadata
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    itinerary_days = relationship("ItineraryDay", back_populates="destination")
    local_transports = relationship("LocalTransportation", back_populates="destination")


# ==================== Travel Itineraries ====================
class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text, nullable=True)

    # Trip Details
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    departure_city = Column(String)

    # Trip Configuration
    travel_theme = Column(SQLEnum(TravelTheme))
    budget_allocated = Column(Float, nullable=True)

    # Status
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="itineraries")
    itinerary_days = relationship("ItineraryDay", back_populates="itinerary")
    budgets = relationship("Budget", back_populates="itinerary")


class ItineraryDay(Base):
    __tablename__ = "itinerary_days"

    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"))
    destination_id = Column(Integer, ForeignKey("destinations.id"))

    # Day Details
    day_number = Column(Integer)
    date = Column(DateTime)

    # Transportation
    arrival_transport_id = Column(Integer, ForeignKey("long_distance_transportations.id"), nullable=True)
    departure_transport_id = Column(Integer, ForeignKey("long_distance_transportations.id"), nullable=True)

    # Activities
    activities = Column(JSON, default=[])  # {"time": "10:00", "place": "museum", "duration": 120}
    notes = Column(Text, nullable=True)

    # Relationships
    itinerary = relationship("Itinerary", back_populates="itinerary_days")
    destination = relationship("Destination", back_populates="itinerary_days")
    arrival_transport = relationship("LongDistanceTransportation", foreign_keys=[arrival_transport_id])
    departure_transport = relationship("LongDistanceTransportation", foreign_keys=[departure_transport_id])


# ==================== Long Distance Transportation ====================
class LongDistanceTransportation(Base):
    __tablename__ = "long_distance_transportations"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(SQLEnum(TransportType))

    # Route Details
    departure_city = Column(String)
    arrival_city = Column(String)
    departure_time = Column(DateTime)
    arrival_time = Column(DateTime)
    duration_minutes = Column(Integer)

    # Pricing
    price = Column(Float)
    currency = Column(String, default="KRW")

    # Provider Information
    provider = Column(String)  # Airline, Railway Company, etc.
    provider_code = Column(String, nullable=True)  # Flight number, train number

    # Booking Information
    booking_methods = Column(JSON)  # [
    #   {
    #     "platform": "Official Website",
    #     "url": "https://...",
    #     "how_to": "Direct booking"
    #   }
    # ]

    # QR Codes for Booking
    booking_qr_links = Column(JSON, nullable=True)  # {
    #   "official_website": "https://...",
    #   "travel_sites": [{...}],
    #   "app_download": "https://..."
    # }

    # Directions
    directions = Column(String, nullable=True)  # "Kim Po Terminal 2 → Jeju Airport"

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ==================== Local Transportation ====================
class LocalTransportation(Base):
    __tablename__ = "local_transportations"

    id = Column(Integer, primary_key=True, index=True)
    destination_id = Column(Integer, ForeignKey("destinations.id"))
    city = Column(String)
    transport_type = Column(SQLEnum(LocalTransportType))

    # Route Information
    route_number = Column(String, nullable=True)  # "600 Bus", "Line 1 Subway"
    route_details = Column(JSON, nullable=True)  # List of stops/stations

    # Schedule & Frequency
    frequency = Column(String)  # "Every 30 minutes", "Peak: 5-10 min"
    operating_hours = Column(JSON)  # {"start": "05:30", "end": "23:30"}

    # Pricing
    fare = Column(Float)
    currency = Column(String, default="KRW")

    # Payment Methods
    payment_methods = Column(JSON)  # ["cash", "card", "app"]
    card_types = Column(JSON, nullable=True)  # ["T-money", "Naver Pay"]

    # Taxi Specific
    base_fare = Column(Float, nullable=True)
    distance_per_km = Column(Float, nullable=True)
    time_unit_fare = Column(Float, nullable=True)
    calling_apps = Column(JSON, nullable=True)  # ["KakaoT", "Naver Map"]
    tip_culture = Column(String, nullable=True)  # "Optional", "Required", "Not Needed"

    # Mobile Apps
    app_download_links = Column(JSON, nullable=True)  # {
    #   "ios": "https://apps.apple.com/...",
    #   "android": "https://play.google.com/..."
    # }

    # Useful Links
    useful_links = Column(JSON, nullable=True)  # {
    #   "timetable": "https://...",
    #   "route_info": "https://...",
    #   "card_shop": "https://..."
    # }

    # Directions
    directions = Column(String, nullable=True)

    # Relationships
    destination = relationship("Destination", back_populates="local_transports")


# ==================== QR Codes ====================
class QRCode(Base):
    __tablename__ = "qr_codes"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, unique=True, index=True)
    qr_code_path = Column(String)  # /static/qr_codes/...
    label = Column(String)  # "Hotel Booking", "Bus App Download"
    category = Column(String)  # "destination", "transportation", "local_transport"
    related_id = Column(Integer, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# ==================== Budget ====================
class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"))

    # Budget Items
    category = Column(String)  # "flight", "accommodation", "meal", "activity", "transport"
    item_name = Column(String)
    estimated_cost = Column(Float)
    actual_cost = Column(Float, nullable=True)
    currency = Column(String, default="KRW")

    # Notes
    notes = Column(Text, nullable=True)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    itinerary = relationship("Itinerary", back_populates="budgets")
