# Apex Auto — Car Dealership Inventory System

A full-stack Car Dealership Inventory System built following **Test-Driven Development (TDD)** principles. It features a RESTful API backend built with Python (FastAPI), SQLAlchemy ORM, and MySQL database, alongside a single-page frontend application built with HTML5, CSS3, JavaScript (ES6+), and Tailwind CSS.

---

## 🌟 Features

- **JWT Authentication & Role-Based Access Control**: Secure token-based access with `USER` and `ADMIN` role distinction.
- **Vehicle Catalog & Search**: Browse vehicles with multi-field filtering by make, model, category, and price range.
- **Inventory Management**:
  - Regular users can purchase vehicles (decrements stock quantity; purchase disabled when stock is 0).
  - Admin users can add new vehicles, update vehicle details, delete listings, and restock quantities.
- **Test-Driven Development (TDD)**: Comprehensive unit and integration test suites using `pytest` for the backend and `Jest` for the frontend.

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Backend Framework** | Python 3.11 + FastAPI |
| **ORM** | SQLAlchemy 2.0 |
| **Database** | MySQL Server (via PyMySQL driver) |
| **Auth** | JWT (`pyjwt`) + `passlib` bcrypt password hashing |
| **Backend Testing** | `pytest` + `pytest-cov` + `httpx` (37 tests, 93% coverage) |
| **Frontend** | HTML5, Vanilla JavaScript (ES6+), Tailwind CSS |
| **Frontend Testing** | `Jest` + `jsdom` (8 tests) |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.11+**
- **MySQL Server** (running on `localhost:3306`)
- **Node.js 18+**

### 1. Database Setup

Ensure your local MySQL service is running, then execute the database creation script:

```bash
cd backend
python create_db.py
```

### 2. Backend Setup & Server Execution

```bash
cd backend

# Create & activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1   # On Windows PowerShell

# Install dependencies
pip install -r requirements.txt -r requirements-test.txt

# Run FastAPI development server
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`. Interactive OpenAPI documentation is accessible at `http://localhost:8000/api/docs`.

### 3. Frontend Execution

The frontend is built using standard ES modules and Tailwind CSS CDN. You can serve the static files using Python's built-in HTTP server or Live Server:

```bash
cd frontend
python -m http.server 5000
```

Open `http://localhost:5000` in your web browser.

---

## 🧪 Running Tests (TDD Verification)

### Backend Tests (pytest)

```bash
cd backend
.\venv\Scripts\pytest --cov=app tests/
```

### Frontend Tests (Jest)

```bash
cd frontend
npm test
```

---

## 🔑 Default Credentials

Upon startup, the database is seeded automatically with the following accounts:

| Role | Email | Password |
|---|---|---|
| **Admin** | `admin@dealership.com` | `Admin@123` |
| **User** | `user@dealership.com` | `User@123` |

---

## 📋 API Endpoints Summary

### Auth
- `POST /api/auth/register` — Register a new user
- `POST /api/auth/login` — Login & receive JWT access token

### Vehicles (🔒 Protected)
- `GET /api/vehicles` — View all vehicles
- `GET /api/vehicles/search` — Search vehicles (`?make=&model=&category=&min_price=&max_price=`)
- `POST /api/vehicles` — Add new vehicle (**Admin Only**)
- `PUT /api/vehicles/{id}` — Update vehicle details (**Admin Only**)
- `DELETE /api/vehicles/{id}` — Delete vehicle (**Admin Only**)

### Inventory (🔒 Protected)
- `POST /api/vehicles/{id}/purchase` — Purchase vehicle (decreases stock)
- `POST /api/vehicles/{id}/restock` — Restock vehicle (**Admin Only**)

---

## 🤖 My AI Usage

### AI Tools Used
- **Antigravity AI (powered by Google DeepMind / Claude 3.5)**: Used as an interactive pair-programming subagent throughout the entire lifecycle of this project.

### How AI Was Used
1. **Architecture & Schema Design**: AI assisted in drafting the SQLAlchemy ORM models, Pydantic validation schemas, and establishing the database relational structure (Users, Vehicles, Transactions).
2. **Test-Driven Development (TDD)**: AI helped draft the unit test cases (`test_password_utils.py`, `test_jwt_utils.py`, `test_auth_service.py`, `test_vehicle_service.py`) and API route integration test cases (`test_auth_routes.py`, `test_vehicle_routes.py`) prior to implementation in a strict Red-Green-Refactor cycle.
3. **Frontend Component & Styling Assistance**: AI generated modern, responsive Tailwind CSS layouts with dark-glass aesthetic accents and glassmorphism styling for `dashboard.html` and `admin.html`.
4. **Git Co-Authorship**: For commits involving AI-generated boilerplate, unit tests, and structural logic, the following co-author trailer was included in Git commit messages:

```
Co-authored-by: Antigravity AI <antigravity-ai@google.com>
```

### Reflections on AI Impact
Utilizing AI as a pair programmer significantly accelerated the TDD feedback loop. Drafting comprehensive edge-case unit tests before writing business logic ensured that edge cases—such as out-of-stock purchases, unauthorized admin route access, and duplicate email registrations—were caught and handled immediately.
