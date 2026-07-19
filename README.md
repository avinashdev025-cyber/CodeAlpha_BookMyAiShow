# 🎟️ BookMyAiShow - Premium AI Event Registration System

BookMyAiShow is a high-fidelity, secure, and modern event booking application designed to manage registrations for next-generation AI events, hackathons, and masterclasses. 

It features a luxurious Red, White, and Black dark theme (similar in quality to Vercel, Linear, or GitHub Dark) with smooth, responsive layouts, hover scales, and interactive states.

---

## ✨ Key Features

- **🔒 Advanced Auth System**:
  - Secure standard Username/Password logins.
  - Full **Google OAuth (Sign In with Google)** integration.
  - Safe automatic logins after registration with multiple authentication backend support.
- **⚡ Seat Capacity & Concurrent Bookings**:
  - Automated seat-tracking logic showing `Registered Count / Total Capacity` for every event.
  - Model-level validators preventing registrations once capacity limits are reached.
  - **Atomic Transaction Locks (`select_for_update`)** protecting booking requests from concurrent race conditions.
- **🎨 Premium Dark Theme UI/UX**:
  - Full Red, White, and Black custom styling ([styles.css](static/css/styles.css)) with custom glowing borders, soft shadows, and typography.
  - Clean page-entry animations and active navigation headers.
  - Responsive layout optimized for desktop, tablet, and mobile displays.
  - Alternating list tables and status badges on the user dashboard.
- **📊 Interactive Dashboard**:
  - Real-time seat meters on the homepage.
  - Custom user panel showing registered events with active/cancelled states.
  - Instant one-click cancellation with immediate seat release.
- **🗄️ Zero-Configuration Database**:
  - Connects to **PostgreSQL** automatically if credentials exist in `.env`.
  - Fallbacks seamlessly to local **SQLite** for instant zero-setup local runs.

---

## 🛠️ Technology Stack

- **Backend Framework**: Django >= 5.0 (Python 3.11+)
- **Database**: SQLite (Local Dev) / PostgreSQL (Production)
- **Frontend**: HTML5, Vanilla CSS3 (Custom Variables & Keyframes), Javascript
- **Authentication**: `django-allauth` for Google Sign-In support
- **Environment**: `python-dotenv` for loading database/secret environment variables

---

## 🚀 Setup & Installation Instructions

Follow these quick commands to spin up the project locally:

### 1. Initialize Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install requirements
pip install -r requirements.txt
```

### 2. Apply Migrations & Set Up Database
```bash
python manage.py migrate
```

### 3. Seed Default Data & Admin Users
This seeds the application with **11 realistic high-capacity AI events** (each with 50+ seats availability) and creates a default superuser:
```bash
python seed_db.py
```
- **Default Superuser**: `admin`
- **Default Password**: `password123`

### 4. Launch the Development Server
```bash
python manage.py runserver
```
Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your browser to explore the portal!

---

## 🧪 Testing the Application
The codebase includes comprehensive unit tests verifying registration logic, constraint validation, concurrency handling, and page rendering. Run tests using:
```bash
python manage.py test events
```

---

## 📁 Project Structure
```text
event-registration-system/
├── event_system/            # Main settings and configuration routing
│   ├── settings.py          # Database credentials, auth backends & oauth keys
│   └── urls.py              # Root URL patterns (events & django-allauth)
├── events/                  # Core application logic
│   ├── models.py            # Event and Registration database models
│   ├── views.py             # Dashboards, bookings, list/detail views
│   └── tests.py             # 10 comprehensive unit tests
├── static/                  
│   ├── css/styles.css       # Premium Red, White, and Black stylesheet
│   └── images/logo.png      # Highlighted, memorable brand logo
└── templates/               # Django template templates
```
