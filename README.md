# Frist-website
# 🔧 Fixio - AI Electronics Repair Assistant

![FixAI Banner](assets/banner.png)

## 📌 Overview

FixAI is an AI-powered electronics repair platform that helps users identify damaged electronic components using image scanning and artificial intelligence.

Users can upload or scan images of TVs, laptops, desktop motherboards, smartphones, and other electronic devices. The AI detects damaged components, explains their purpose, suggests repair solutions, and recommends replacement parts and nearby service centers.

---

# ✨ Features

## 🤖 AI Component Detection
- Scan motherboard images
- Detect damaged electronic components
- Identify ICs, Capacitors, MOSFETs, Diodes, Resistors, Fuses, Relays, etc.

---

## 🔍 OCR Recognition
- Read component numbers
- Identify part numbers
- Detect package type

---

## 🧠 AI Assistant

Ask questions like:

- Why is my TV not turning on?
- What is this IC?
- How do I replace this capacitor?
- Why did this component fail?
- What tools are required?

---

## 📖 Repair Guide

- Step-by-step repair instructions
- Required tools
- Safety precautions
- Repair difficulty
- Estimated repair time

---

## 🛒 Marketplace

Find replacement components

- Component Name
- Price
- Stock
- Compatible Parts
- Buy Online

---

## 🏪 Nearby Stores

Locate nearby electronics shops.

- Address
- Phone
- Ratings
- Maps

---

## 🏢 Service Centers

Find authorized service centers.

Examples

- Samsung
- LG
- Sony
- Dell
- HP
- Lenovo

---

## 📊 Scan History

- Previous scans
- Saved reports
- Repair history

---

# 🖥️ Tech Stack

## Frontend

- React
- HTML5
- CSS3
- Tailwind CSS
- JavaScript

---

## Backend

- Python
- FastAPI
- SQLAlchemy

---

## Database

- SQLite
- PostgreSQL (Future)

---

## AI

- YOLO
- OpenCV
- PaddleOCR
- GPT API / Gemini API

---

# 📁 Project Structure

```
FixAI/

backend/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── ai_engine.py
├── routers/
├── static/
└── fixai.db

frontend/
│
├── assets/
├── components/
├── products/
├── scans/
└── stores/

README.md
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/yourusername/FixAI.git
```

---

## Create Virtual Environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux/macOS

```bash
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Backend

```bash
uvicorn main:app --reload
```

Backend

```
http://127.0.0.1:8000
```

API Docs

```
http://127.0.0.1:8000/docs
```

---

# 🎯 Future Features

- Live Camera Detection
- PCB Analysis
- Thermal Detection
- Voice Assistant
- AR Repair Guidance
- Technician Dashboard
- Inventory Management
- AI Repair Cost Estimation
- Community Forum

---

# 📸 Screens

- Home
- Login
- Register
- Dashboard
- AI Scanner
- Scan Result
- Component Details
- AI Assistant
- Repair Guide
- Marketplace
- Service Centers
- Profile
- Settings

---

# 🤝 Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to your branch
5. Open a Pull Request

---

# 📄 License

This project is licensed under the MIT License.

---

# 👨‍💻 Author

**Project Name:** FixAI

AI Powered Electronics Repair Assistant

Made with ❤️ using Python, FastAPI, React, and AI.
