from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any, Dict
from datetime import datetime

# Auth Schemas
class UserRegister(BaseModel):
    full_name: str
    email: str
    password: str
    phone: Optional[str] = None
    location: Optional[str] = "Chennai, India"

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str]
    location: Optional[str]
    avatar_url: Optional[str]
    role: str

    class Config:
        from_attributes = True

# Scan Schemas
class BoundingBox(BaseModel):
    id: str
    label: str
    part_number: str
    status: str # Damaged, Warning, Healthy
    severity: str
    confidence: float
    x: float # % coordinates
    y: float
    width: float
    height: float
    issue_description: str

class DamageReportOut(BaseModel):
    id: int
    device_name: str
    component_name: str
    part_number: str
    image_path: str
    damage_status: str
    confidence_percentage: float
    severity_level: str
    estimated_repair_cost: str
    estimated_repair_time: str
    bounding_boxes: List[Dict[str, Any]]
    damage_cause: str
    repair_steps_summary: List[str]
    datasheet_url: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

# Component Schemas
class ComponentOut(BaseModel):
    id: int
    name: str
    part_number: str
    category: str
    purpose: str
    working_principle: str
    specifications: Dict[str, Any]
    pin_diagram: List[Dict[str, Any]]
    datasheet_url: Optional[str]
    common_failures: List[str]
    replacement_procedure: str
    safety_notes: str
    package_type: str
    image_url: Optional[str]

    class Config:
        from_attributes = True

# Chat Schemas
class ChatMessage(BaseModel):
    session_id: str
    message: str
    image_url: Optional[str] = None

class ChatResponse(BaseModel):
    session_id: str
    reply: str
    suggested_actions: Optional[List[str]] = None
    timestamp: datetime

# Repair Guide Schemas
class RepairGuideOut(BaseModel):
    id: int
    title: str
    difficulty: str
    repair_time: str
    required_tools: List[Dict[str, str]]
    safety_precautions: List[str]
    steps: List[Dict[str, Any]]
    video_url: Optional[str]

    class Config:
        from_attributes = True

# Product Schemas
class ProductOut(BaseModel):
    id: int
    name: str
    part_number: str
    category: str
    price: float
    price_formatted: str
    stock_status: str
    stock_quantity: int
    compatibility_info: str
    rating: float
    image_url: Optional[str]

    class Config:
        from_attributes = True

# Service Center Schemas
class ServiceCenterOut(BaseModel):
    id: int
    store_name: str
    address: str
    city: str
    state: str
    phone: str
    opening_hours: str
    rating: float
    review_count: int
    lat: float
    lng: float
    distance_km: float
    is_authorized: bool
    image_url: Optional[str]

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    store_id: int
    user_name: str
    phone: str
    device_type: str
    issue_description: str
    preferred_date: str
    preferred_time: str
