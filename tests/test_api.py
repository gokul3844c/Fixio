import os
import io
import uuid
import pytest
from PIL import Image
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "Fixio" in data["service"]

def test_auth_flow():
    email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    password = "TestPassword123!"

    # 1. Register User
    reg_res = client.post("/api/auth/register", json={
        "full_name": "Test User",
        "email": email,
        "password": password
    })
    assert reg_res.status_code == 200
    token = reg_res.json()["access_token"]
    assert token is not None

    # 2. Login User
    login_res = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })
    assert login_res.status_code == 200
    assert login_res.json()["access_token"] == token

    # 3. Profile /me Endpoint
    me_res = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me_res.status_code == 200
    assert me_res.json()["email"] == email

def test_scanner_vision_and_motherboard_detection():
    email = f"scanner_{uuid.uuid4().hex[:6]}@example.com"
    reg_res = client.post("/api/auth/register", json={
        "full_name": "Scanner Tester",
        "email": email,
        "password": "Password123!"
    })
    token = reg_res.json()["access_token"]

    # Test 1: Motherboard / PCB image (routed to component_datasheet mode without showing property damage)
    pcb_img = Image.new("RGB", (200, 200), color=(20, 180, 80))
    img_bytes = io.BytesIO()
    pcb_img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    scan_res = client.post(
        "/api/scan",
        files={"file": ("pcb_test.jpg", img_bytes, "image/jpeg")},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert scan_res.status_code == 200
    scan_data = scan_res.json()
    assert scan_data["mode"] == "component_datasheet"
    assert len(scan_data["issues_json"]) == 0

    # Test 2: Datasheet manual search API
    ds_res = client.get("/api/components/search?part_number=LM317")
    assert ds_res.status_code == 200
    ds_data = ds_res.json()
    assert ds_data["found"] is True
    assert ds_data["part_number"] == "LM317"
    assert ds_data["manufacturer"] == "Texas Instruments"

def test_record_ownership_protection():
    email_a = f"alice_{uuid.uuid4().hex[:6]}@example.com"
    email_b = f"bob_{uuid.uuid4().hex[:6]}@example.com"

    reg_a = client.post("/api/auth/register", json={"full_name": "Alice", "email": email_a, "password": "Password123!"})
    token_a = reg_a.json()["access_token"]

    reg_b = client.post("/api/auth/register", json={"full_name": "Bob", "email": email_b, "password": "Password123!"})
    token_b = reg_b.json()["access_token"]

    img_bytes = io.BytesIO()
    Image.new("RGB", (200, 200), color=(180, 180, 180)).save(img_bytes, format="JPEG")
    img_bytes.seek(0)

    scan_res = client.post(
        "/api/scan",
        files={"file": ("wall.jpg", img_bytes, "image/jpeg")},
        headers={"Authorization": f"Bearer {token_a}"}
    )
    report_id = scan_res.json()["id"]

    # User A accesses own report -> 200 OK
    own_res = client.get(f"/api/scan/{report_id}", headers={"Authorization": f"Bearer {token_a}"})
    assert own_res.status_code == 200

    # User B attempts to access User A report -> 403 Forbidden
    other_res = client.get(f"/api/scan/{report_id}", headers={"Authorization": f"Bearer {token_b}"})
    assert other_res.status_code == 403

def test_service_centers_haversine_and_appointments():
    email = f"apt_{uuid.uuid4().hex[:6]}@example.com"
    reg_res = client.post("/api/auth/register", json={"full_name": "Apt Tester", "email": email, "password": "Password123!"})
    token = reg_res.json()["access_token"]

    # Haversine distance check
    sc_res = client.get("/api/service-centers?user_lat=13.0827&user_lng=80.2707")
    assert sc_res.status_code == 200
    centers = sc_res.json()
    assert len(centers) > 0
    assert "distance_km" in centers[0]

    # Appointment booking check
    store_id = centers[0]["id"]
    apt_res = client.post(
        "/api/service-centers/book-appointment",
        json={
            "store_id": store_id,
            "preferred_date": "2026-10-10",
            "preferred_time": "11:00 AM",
            "notes": "Testing appointment booking."
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert apt_res.status_code == 200
    assert "appointment_id" in apt_res.json()

def test_repair_guides_safety_and_404():
    # Category matching with safety check
    guide_res = client.get("/api/guides/match?category=electrical_hazard&severity=high")
    assert guide_res.status_code == 200
    guides = guide_res.json()
    assert len(guides) > 0
    assert "SAFETY WARNING" in guides[0]["when_to_stop"]

    # Non-existent guide ID -> 404 Not Found
    notFound_res = client.get("/api/guides/99999")
    assert notFound_res.status_code == 404
