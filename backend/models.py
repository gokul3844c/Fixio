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
    role = Column(String(20), default="technician")
    created_at = Column(DateTime, default=datetime.utcnow)

    damage_reports = relationship("DamageReport", back_populates="user")
    chat_histories = relationship("ChatHistory", back_populates="user")
    notifications = relationship("Notification", back_populates="user")

class Component(Base):
    __tablename__ = "components"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    part_number = Column(String(50), nullable=False, index=True)
    category = Column(String(50), nullable=False) # IC, Capacitor, Resistor, MOSFET, Diode, Fuse, Connector
    purpose = Column(Text, nullable=False)
    working_principle = Column(Text, nullable=False)
    specifications = Column(JSON, nullable=False) # dict of specs e.g. voltage, current, pin count
    pin_diagram = Column(JSON, nullable=False) # pin list & description
    datasheet_url = Column(String(255), nullable=True)
    common_failures = Column(JSON, nullable=False) # list of strings
    replacement_procedure = Column(Text, nullable=False)
    safety_notes = Column(Text, nullable=False)
    package_type = Column(String(50), default="TO-220")
    image_url = Column(String(255), nullable=True)

    damage_reports = relationship("DamageReport", back_populates="component")
    repair_guides = relationship("RepairGuide", back_populates="component")
    products = relationship("Product", back_populates="component")

class DamageReport(Base):
    __tablename__ = "damage_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    device_name = Column(String(100), default="Motherboard PCB Rev 3.2")
    component_id = Column(Integer, ForeignKey("components.id"), nullable=True)
    component_name = Column(String(100), default="Voltage Regulator IC")
    part_number = Column(String(50), default="LM7805")
    image_path = Column(String(255), nullable=False)
    damage_status = Column(String(50), default="Damaged - Burned IC") # Damaged, Warning, Healthy
    confidence_percentage = Column(Float, default=94.5)
    severity_level = Column(String(20), default="High") # High, Medium, Low
    estimated_repair_cost = Column(String(50), default="$15 - $30 (₹120 - ₹250)")
    estimated_repair_time = Column(String(50), default="30 - 60 mins")
    bounding_boxes = Column(JSON, nullable=False) # list of detected items with coords, label, severity
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
    component_id = Column(Integer, ForeignKey("components.id"), nullable=True)
    difficulty = Column(String(20), default="Intermediate") # Beginner, Intermediate, Advanced
    repair_time = Column(String(50), default="30 - 60 mins")
    required_tools = Column(JSON, nullable=False) # list of tool dicts: {name, icon}
    safety_precautions = Column(JSON, nullable=False) # list of strings
    steps = Column(JSON, nullable=False) # list of step dicts: {step_number, title, detail, tip}
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
    price_formatted = Column(String(30), default="$2.50 / ₹20")
    stock_status = Column(String(30), default="In Stock")
    stock_quantity = Column(Integer, default=150)
    compatibility_info = Column(String(255), default="Compatible with 5V Regulated Power Circuits")
    rating = Column(Float, default=4.8)
    image_url = Column(String(255), nullable=True)

    component = relationship("Component", back_populates="products")

class ServiceCenter(Base):
    __tablename__ = "service_centers"

    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String(100), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(50), nullable=False)
    state = Column(String(50), nullable=False)
    phone = Column(String(30), nullable=False)
    opening_hours = Column(String(100), default="9:00 AM - 8:00 PM")
    rating = Column(Float, default=4.7)
    review_count = Column(Integer, default=128)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    distance_km = Column(Float, default=1.5)
    is_authorized = Column(Boolean, default=True)
    image_url = Column(String(255), nullable=True)

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    session_id = Column(String(64), nullable=False, index=True)
    sender = Column(String(20), nullable=False) # user or ai
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="chat_histories")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(100), nullable=False)
    message = Column(Text, nullable=False)
    type = Column(String(30), default="info") # info, success, warning, error
    is_read = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="notifications")
