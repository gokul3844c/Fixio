from pydantic import BaseModel, EmailStr
from typing import List, Optional, Any, Dict
from datetime import datetime

# Standard API Response Wrapper
class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None

# Auth Schemas
class UserRegister(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: Optional[str] = None
    location: Optional[str] = "Chennai, India"


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class GoogleLogin(BaseModel):
    credential: Optional[str] = None
    token: Optional[str] = None


class UserOut(BaseModel):
    id: int
    full_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    avatar_url: Optional[str] = None
    role: str = "user"

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

# Scan Result Schemas matching requested format
class AIScanAnalysisOutput(BaseModel):
    analysisStatus: str # completed, unsupported_object, unclear_image, analysis_failed
    component_type: str = "Property Structure"
    damage_status: str = "Analysis Completed"
    confidence_score: float = 0.85
    issue_title: str = "Damage Inspection"
    severity: str = "medium" # low, medium, high
    location_detected: str = "Inspected Area"
    recommended_action: str = "Inspect and repair according to guidance"
    estimated_cost: str = "$100 - $300"
    safety_warning: str = "Always turn off relevant utilities before inspection."
    repair_steps: List[str] = []
    raw_message: Optional[str] = None

class ScanIssue(BaseModel):
    title: str
    category: str
    location: str
    severity: str # low, medium, high
    confidence: float # e.g. 0.85
    possibleCauses: List[str]
    recommendedActions: List[str]
    safetyWarning: Optional[str] = None

class ScanResultPayload(BaseModel):
    scanId: str
    issues: List[ScanIssue]
    disclaimer: str = "Image analysis is preliminary and does not replace an in-person inspection."

class DamageReportOut(BaseModel):
    id: int
    scan_id: str
    mode: Optional[str] = "property_damage"
    device_name: str
    component_name: str
    manufacturer: Optional[str] = None
    part_number: str
    image_path: str
    damage_status: str
    confidence_percentage: float
    severity_level: str
    estimated_repair_cost: str
    estimated_repair_time: str
    bounding_boxes: List[Dict[str, Any]]
    issues_json: List[Dict[str, Any]]
    disclaimer: str
    damage_cause: str
    repair_steps_summary: List[str]
    datasheet_url: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Component Schemas
class ComponentOut(BaseModel):
    id: int
    name: str
    part_number: str
    manufacturer: Optional[str] = "Original Manufacturer"
    category: str
    purpose: str
    working_principle: str
    specifications: Dict[str, Any]
    pin_diagram: List[Dict[str, Any]]
    datasheet_url: Optional[str] = None
    common_failures: List[str]
    replacement_procedure: str
    safety_notes: str
    package_type: str
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

class DatasheetSearchOut(BaseModel):
    found: bool
    manufacturer: Optional[str] = None
    part_number: Optional[str] = None
    name: Optional[str] = None
    category: Optional[str] = None
    specifications: Optional[Dict[str, Any]] = None
    datasheet_url: Optional[str] = None
    confidence_percentage: float = 0.0
    original_image_url: Optional[str] = None
    message: str

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
    category: str
    difficulty: str
    repair_time: str
    short_explanation: Optional[str] = None
    common_causes: Optional[List[str]] = None
    signs_to_check: Optional[List[str]] = None
    safe_diy_actions: Optional[List[str]] = None
    professional_actions: Optional[List[str]] = None
    required_tools: List[Dict[str, str]]
    safety_precautions: List[str]
    estimated_cost_range: Optional[str] = None
    when_to_stop: Optional[str] = None
    related_service_categories: Optional[List[str]] = None
    steps: List[Dict[str, Any]]
    video_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    class Config:
        from_attributes = True

# Review Schemas
class ReviewCreate(BaseModel):
    service_center_id: int
    rating: int # 1-5
    comment: str
    verified_job: Optional[bool] = True

class ReviewOut(BaseModel):
    id: int
    service_center_id: int
    user_id: int
    user_name: str
    rating: int
    comment: str
    verified_job: bool
    provider_response: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

# Service Center Schemas
class ServiceCenterOut(BaseModel):
    id: int
    store_name: str
    category: str
    address: str
    city: str
    state: str
    phone: str
    opening_hours: str
    is_open_now: bool
    rating: float
    review_count: int
    lat: float
    lng: float
    distance_km: float
    is_authorized: bool
    image_url: Optional[str] = None
    reviews: List[ReviewOut] = []

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    store_id: int
    preferred_date: str
    preferred_time: str
    user_name: Optional[str] = None
    phone: Optional[str] = None
    device_type: Optional[str] = None
    issue_description: Optional[str] = None
    notes: Optional[str] = None

# Product Schemas
class ProductCreate(BaseModel):
    name: str
    part_number: str
    category: str
    price: float
    price_formatted: Optional[str] = None
    stock_status: Optional[str] = "In Stock"
    stock_quantity: Optional[int] = 100
    compatibility_info: Optional[str] = ""
    rating: Optional[float] = 5.0
    image_url: Optional[str] = ""

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
    image_url: Optional[str] = None

    class Config:
        from_attributes = True

