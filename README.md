# 🏘️ Fixio — Compound & Property Damage Detection, Repair Guides & Service Centers

Fixio is an AI-powered compound & property damage inspection platform that enables homeowners, property managers, and civil inspectors to detect structural defects, wall cracks, water seepage, roof tile damage, and electrical hazards through automated image analysis.

---

## 📌 Technology Stack

### Frontend
- **HTML5 & Vanilla CSS3:** SPA layout built using a modern custom Glassmorphism design system.
- **Vanilla JavaScript (ES6+):** SPA module architecture (`app.js`, `scan.js`, `map.js`, `dashboard.js`, `chat.js`, `marketplace.js`).
- **Leaflet.js v1.9.4:** Interactive OpenStreetMap integration with custom markers and popups.
- **Google Identity Services SDK:** Official GIS client for Google OAuth2 sign-in.

### Backend
- **Python 3.12+ / FastAPI:** High-performance asynchronous REST API.
- **SQLite & SQLAlchemy 2.0+:** Relational database storage with ORM models (`User`, `DamageReport`, `ServiceCenter`, `Review`, `Appointment`, `RepairGuide`, `Product`, `ChatHistory`).
- **Pydantic v2:** Strict input validation and structured schema responses.
- **PyJWT:** Standard-compliant JWT authentication and token verification.
- **Pillow (PIL):** Image binary payload verification, pixel tensor analysis, contrast & entropy checking.
- **Google Generative AI (Gemini 2.5 Flash):** Vision-capable multimodal image understanding model.
- **Alembic:** Database migration system.

---

## ✨ Core Features

1. **AI Property Damage Scanner:**
   - Detects wall cracks, dampness, roof tile fractures, and electrical hazards.
   - PIL visual tensor analysis & Google Gemini 2.5 Flash Vision API integration.
   - Detects and rejects unsupported objects (e.g., electronic motherboards, pets, faces) with `analysisStatus: "unsupported_object"`.
   - Rejects pitch black, blurry, or low-contrast photos with `analysisStatus: "unclear_image"`.
   - Displays original uploaded image with severity badges, cost estimates, repair steps, and safety disclaimers.

2. **Verified Authentication & Access Control:**
   - Standard password registration and login with PBKDF2 hashing.
   - Cryptographically verified Google ID token sign-in (`google.oauth2.id_token.verify_oauth2_token`).
   - Cross-account record ownership protection returning `HTTP 403 Forbidden` for unauthorized resource access.

3. **Nearby Service Centers & Map Integration:**
   - Interactive Leaflet map displaying verified contractor locations.
   - Geolocation & dynamic Haversine spatial distance sorting (`user_lat`, `user_lng`).
   - Category filtering (Masonry & Structural, Waterproofing & Plumbing, Roofing & Tiles, Electrical).
   - Database-persisted appointment booking system (`Appointment` model).

4. **Matched Repair Guides:**
   - Categorized repair steps, required tools, and estimated costs.
   - Enforces strict safety rules for high-risk hazards (prohibiting DIY for high-voltage or major structural fractures).

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Variables (Optional `.env`)
```env
SECRET_KEY=your_secure_jwt_secret_key
GOOGLE_CLIENT_ID=your_google_oauth2_client_id
GEMINI_API_KEY=your_gemini_api_key
ALLOWED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
```

### 3. Run Application Server
```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```
Open [http://localhost:8000](http://localhost:8000) in your web browser.

### 4. Run Automated API Tests
```bash
python -m pytest tests/test_api.py
```
