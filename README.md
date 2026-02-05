# ZEN-PDF ⚡
### Enterprise-Grade PDF Manipulation Suite

![Status](https://img.shields.io/badge/Status-Active-success)
![Version](https://img.shields.io/badge/Version-1.0.0-blue)
![License](https://img.shields.io/badge/License-MIT-purple)

**Zen-PDF** is a high-performance, asynchronous web application designed for complex PDF operations. Built with a **Flask** core and powered by a **Celery + Redis** event-driven architecture, it handles heavy document processing in the background without blocking the user interface.

Wrapped in a **Cyberpunk/Futuristic UI**, it features a custom "Glassmorphism" design system, smooth page transitions, and a responsive grid layout.

---

## 🚀 Features

### Core Modules
* **🔗 Merge PDF:** Combine multiple documents into a single unified file.
* **✂️ Split PDF:** (In Progress) Fragment documents into individual pages.
* **📉 Compress:** (In Progress) Optimize data density and remove redundant artifacts.
* **🔄 Convert:** (In Progress) Raster image to standardized PDF conversion.

### Technical Capabilities
* **Asynchronous Processing:** Uses **Celery Workers** to handle file operations in the background.
* **Real-time Status Polling:** Frontend polls the **REST API** to update progress bars without page reloads.
* **Enterprise Security:** CSRF protection, secure filename hashing, and role-based access control (RBAC).
* **Admin Dashboard:** Dedicated interface for system monitoring, user management, and server logs.

---

## 🛠️ Tech Stack

### Backend
* **Framework:** Python Flask (Blueprints Architecture)
* **Database:** SQLite (SQLAlchemy ORM)
* **Async Queue:** Celery
* **Message Broker:** Redis
* **Authentication:** Flask-Login + Bcrypt

### Frontend
* **Design System:** Custom CSS "Zen Grid" & "Neon Variables"
* **Interactions:** Vanilla JavaScript (ES6 Modules)
* **Fonts:** JetBrains Mono (Tech), Inter (UI)

---

## ⚡ Installation & Setup

### Prerequisites
* Python 3.10+
* Redis (Must be running locally)

### 1. Clone the Repository
```bash
git clone [https://github.com/src-neil/zen-pdf.git](https://github.com/src-neil/zen-pdf.git)
cd zen-pdf
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python -m venv venv
source venv/bin/activate  

# Activate (Windows)
.\venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt 
```

### 4. Configure Environment Variables
```bash
Create a .env file in the root directory (optional, defaults provided in config.py):
SECRET_KEY=your_secret_key
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

## 🏃‍♂️ Running the Application

This system requires **two terminals** running simultaneously.

### Terminal 1: The Background Worker (The Chef)
This processes the heavy files.

```powershell
# Windows (Solo Pool required)
celery -A celery_worker.celery worker --pool=solo --loglevel=info

# Linux/Mac
celery -A celery_worker.celery worker --loglevel=info
```
### Terminal 2: The Web Server (The Waiter)
This serves the UI and API.

```powershell
python run.py
```
Access the application at: http://127.0.0.1:5000

## 📂 Project Structure

```text
zen-pdf/
├── app/
│   ├── blueprints/
│   │   ├── admin/
│   │   │   ├── __init__.py
│   │   │   ├── forms.py
│   │   │   └── routes.py
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       └── endpoints.py
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── forms.py
│   │   │   └── routes.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── routes.py
│   │   └── pdf_engine/
│   │       ├── workers/
│   │       │   ├── __init__.py
│   │       │   ├── compressor.py
│   │       │   ├── converter.py
│   │       │   ├── editor.py
│   │       │   ├── merger.py
│   │       │   └── splitter.py
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       └── tasks.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── activity_log.py
│   │   ├── audit.py
│   │   ├── file_meta.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── api_schema.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── components/
│   │   │   │   ├── _animations.css
│   │   │   │   ├── _buttons.css
│   │   │   │   └── _forms.css
│   │   │   ├── admin.css
│   │   │   └── main.css
│   │   ├── img/
│   │   │   ├── assets/
│   │   │   └── icons/
│   │   ├── js/
│   │   │   ├── modules/
│   │   │   │   ├── file_uploader.js
│   │   │   │   └── ui_interactions.js
│   │   │   ├── main.js
│   │   │   └── pdf_viewer.js
│   │   └── uploads/
│   │       ├── .gitkeep
│   ├── templates/
│   │   ├── admin/
│   │   │   ├── dashboard.html
│   │   │   ├── logs.html
│   │   │   └── users.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── components/
│   │   │   ├── flash_messages.html
│   │   │   ├── footer.html
│   │   │   └── navbar.html
│   │   ├── core/
│   │   │   ├── index.html
│   │   │   ├── landing.html
│   │   │   └── pricing.html
│   │   ├── layouts/
│   │   │   ├── admin_layout.html
│   │   │   └── auth_layout.html
│   │   ├── pdf/
│   │   │   ├── canvas_ui.html
│   │   │   ├── editor_ui.html
│   │   │   ├── result.html
│   │   │   ├── simple_upload.html
│   │   │   └── split_ui.html
│   │   └── base.html
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── constants.py
│   │   ├── decorators.py
│   │   ├── file_handler.py
│   │   └── security.py
│   ├── __init__.py
│   └── extensions.py
├── instance/
│   └── zenpdf.db
├── logs/
│   └── error.log
├── migrations/
│   └── versions/
├── tests/
│   ├── functional/
│   │   └── test_routes.py
│   └── unit/
│       ├── __init__.py
│       ├── conftest.py
│       └── test_models.py
├── .env
├── .gitignore
├── celery_worker.py
├── config.py
├── README.md
├── requirements.txt
└── run.py
```
## 👨‍💻 Author

**Neil (src-neil)**
* **Role:** Full Stack Developer & Ethical Hacker
* **GitHub:** [src-neil](https://github.com/src-neil)

---

*System Status: All Systems Nominal. End of Line.*