from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=True)
    phone = Column(String(30), nullable=True)
    location = Column(String(100), default="Chennai, India")
    avatar_url = Column(String(255), default="/assets/avatars/default.jpg")
    role = Column(String(20), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

    damage_reports = relationship("DamageReport", back_populates="user", cascade="all, delete-orphan")
    chat_histories = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")
    notifications = relationship("Notification", back_populates="user", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="user", cascade="all, delete-orphan")

class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    part_number = Column(String(50), nullable=False, index=True)
    category = Column(String(50), nullable=False) # Wall, Roof, Plumbing, Tile, Paint, Metal, Drainage, Gate, Electrical
    purpose = Column(Text, nullable=False)
    working_principle = Column(Text, nullable=False)
    specifications = Column(JSON, nullable=False)
    pin_diagram = Column(JSON, nullable=False)
    datasheet_url = Column(String(255), nullable=True)
    common_failures = Column(JSON, nullable=False)
    replacement_procedure = Column(Text, nullable=False)
    safety_notes = Column(Text, nullable=False)
    manufacturer = Column(String(100), default="Original Manufacturer")
    package_type = Column(String(50), default="Property Material")
    image_url = Column(String(255), nullable=True)

    damage_reports = relationship("DamageReport", back_populates="component")
    repair_guides = relationship("RepairGuide", back_populates="component")
    products = relationship("Product", back_populates="component")

class DamageReport(Base):
    __tablename__ = "damage_reports"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(String(64), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    mode = Column(String(50), default="property_damage") # property_damage or component_datasheet
    device_name = Column(String(100), default="Compound / Property Wall")
    component_id = Column(Integer, ForeignKey("components.id"), nullable=True)
    component_name = Column(String(100), default="Exterior Masonry Wall")
    manufacturer = Column(String(100), nullable=True)
    part_number = Column(String(50), default="WALL-CRACK-01")
    image_path = Column(String(255), nullable=False)
    damage_status = Column(String(50), default="Damaged - Wall Crack")
    confidence_percentage = Column(Float, default=85.0)
    severity_level = Column(String(20), default="medium") # high, medium, low
    estimated_repair_cost = Column(String(50), default="$50 - $150 (₹4,000 - ₹12,000)")
    estimated_repair_time = Column(String(50), default="2 - 4 hours")
    bounding_boxes = Column(JSON, nullable=False)
    issues_json = Column(JSON, nullable=False) # Structured array matching requested API schema
    disclaimer = Column(Text, default="Image analysis is preliminary and does not replace an in-person inspection.")
    damage_cause = Column(Text, nullable=False)
    repair_steps_summary = Column(JSON, nullable=False)
    datasheet_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="damage_reports")
    component = relationship("Component", back_populates="damage_reports")

class RepairGuide(Base):
    __tablename__ = "repair_guides"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    category = Column(String(50), default="Wall Cracks")
    component_id = Column(Integer, ForeignKey("components.id"), nullable=True)
    difficulty = Column(String(20), default="Intermediate")
    repair_time = Column(String(50), default="2 - 4 hours")
    short_explanation = Column(Text, nullable=True)
    common_causes = Column(JSON, nullable=True)
    signs_to_check = Column(JSON, nullable=True)
    safe_diy_actions = Column(JSON, nullable=True)
    professional_actions = Column(JSON, nullable=True)
    required_tools = Column(JSON, nullable=False)
    safety_precautions = Column(JSON, nullable=False)
    estimated_cost_range = Column(String(50), default="$50 - $200")
    when_to_stop = Column(Text, nullable=True)
    related_service_categories = Column(JSON, nullable=True)
    steps = Column(JSON, nullable=False)
    video_url = Column(String(255), nullable=True)
    thumbnail_url = Column(String(255), nullable=True)

    component = relationship("Component", back_populates="repair_guides")

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    component_id = Column(Integer, ForeignKey("components.id"), nullable=True)
    name = Column(String(100), nullable=False)
    part_number = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    currency = Column(String(10), default="USD")
    price_formatted = Column(String(30), default="$12.50")
    stock_status = Column(String(30), default="In Stock")
    stock_quantity = Column(Integer, default=150)
    compatibility_info = Column(String(255), default="Suitable for concrete wall crack sealing and surface repair.")
    rating = Column(Float, default=4.8)
    image_url = Column(String(255), nullable=True)

    component = relationship("Component", back_populates="products")

class ServiceCenter(Base):
    __tablename__ = "service_centers"

    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String(100), nullable=False)
    category = Column(String(50), default="Masonry & Structural") # Masonry & Structural, Plumbing, Roofing, Electrical, Paints, General Contracting
    address = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    phone = Column(String(30), nullable=False)
    opening_hours = Column(String(100), default="08:00 AM - 07:00 PM")
    is_open_now = Column(Boolean, default=True)
    rating = Column(Float, default=4.7)
    review_count = Column(Integer, default=24)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    distance_km = Column(Float, default=1.5)
    is_authorized = Column(Boolean, default=True)
    image_url = Column(String(255), nullable=True)

    reviews = relationship("Review", back_populates="service_center", cascade="all, delete-orphan")
    appointments = relationship("Appointment", back_populates="service_center", cascade="all, delete-orphan")

class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    service_center_id = Column(Integer, ForeignKey("service_centers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_name = Column(String(100), nullable=False)
    rating = Column(Integer, nullable=False) # 1 to 5
    comment = Column(Text, nullable=False)
    verified_job = Column(Boolean, default=True)
    provider_response = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    service_center = relationship("ServiceCenter", back_populates="reviews")
    user = relationship("User", back_populates="reviews")

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    appointment_code = Column(String(50), unique=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_center_id = Column(Integer, ForeignKey("service_centers.id"), nullable=False)
    preferred_date = Column(String(30), nullable=False)
    preferred_time = Column(String(30), nullable=False)
    notes = Column(Text, nullable=True)
    status = Column(String(30), default="Confirmed") # Confirmed, Pending, Completed, Cancelled
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="appointments")
    service_center = relationship("ServiceCenter", back_populates="appointments")

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(64), nullable=False, index=True)
    sender = Column(String(20), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_histories")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(30), default="info")
    is_read = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")

