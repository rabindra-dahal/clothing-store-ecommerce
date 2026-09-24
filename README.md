# 👕 Threads & Trends API

A modern, enterprise-ready **FastAPI** backend for a cloth shopping e-commerce application. This project features a fully modular architecture, zero-ORM native SQLite persistence, JWT-based security layers, automated `pytest` coverage matrices, and a Continuous Integration (CI) pipeline powered by GitHub Actions.

---

## ✨ Features

- **Anonymous Browsing:** Customers can freely browse clothing items and look up item specifics without authentication.
- **Secure Customer Accounts:** Native `bcrypt` password hashing protects customer accounts on registration (`/auth/signup`) and issues JWT authentication bearer tokens on login (`/auth/login`).
- **Shopping Cart Mechanics:** Authenticated shoppers can stage clothing quantities inside an active list, with automated product stock limits validation checks.
- **Transactional Checkout Engine:** Atomic SQLite transaction statements deduct store inventory quantities and generate secure, detailed payslip receipts.
- **Order History:** Shoppers can securely track and review their historic transaction profiles over time (`GET /orders`).

---

## 📂 Architecture Layout

```text
cloth_store/
├── .github/workflows/
│   └── ci.yml             # GitHub Actions CI Automation Workflow
├── app/
│   ├── config.py          # Environment settings & secrets 
│   ├── database.py        # Native SQLite initializer & table seeding 
│   ├── auth.py            # JWT token creation & secure hash parsing
│   ├── models.py          # Data models (Pydantic payload schemas)
│   ├── routers/
│   │   ├── auth.py        # Authentication routers (signup/login)
│   │   ├── browsing.py    # Public catalog exploration endpoints
│   │   └── cart.py        # Protected shopping, checkout & payment endpoints
│   └── main.py            # API constructor & router assembly core
└── tests/
    ├── conftest.py        # Pytest multi-threaded memory DB fixtures
    └── test_routes.py     # Automated route testing suites
```

---

## 🚀 Getting Started

### 📋 Prerequisites
Ensure you have **Python 3.12+** installed on your workstation.

### 1. Clone & Set Up Environment
Clone this repository to your local directory machine, change into the root folder, and initialize a Python virtual environment:
```bash
# Initialize a local virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Project Dependencies
Install all core application packages along with development and testing dependencies:
```bash
pip install fastapi uvicorn PyJWT bcrypt pytest httpx pytest-cov
```

### 3. Start the Server
Launch the FastAPI backend server application using Uvicorn:
```bash
uvicorn app.main:app --reload
```
*The app will automatically initialize a local `ecommerce.db` SQLite data instance and seed the initial clothing catalog on initial initialization boot.*

---

## 🔍 Interacting and Testing endpoints

### Interactive Swagger UI API Docs
Once your local server instances initialize, direct your web browser over to **[http://127.0.0](http://127.0.0)**. This auto-generates your Swagger UI interface workspace where you can test operations directly.

### 🔐 Authentication Walkthrough inside Swagger:
1. Locate and trigger the **`POST /auth/login`** endpoint using valid signup payload strings.
2. Extract the long, unbroken hash string value assigned inside the `"access_token"` response dictionary block.
3. Scroll to the top right section of the Swagger page, and click the green **Authorize** icon block.
4. Paste your token directly into the value field string and lock authorization. All protected endpoint parameters will seamlessly pass authentication credentials automatically.

---

## 🧪 Testing and Quality Audits

### Run Automated Pytest Suite
Execute the testing routines matrix in verbose mode from your workspace terminal root block:
```bash
pytest -v
```
*Tests are fully thread-safe and isolated to run within an asynchronous `file::memory:` SQLite structure. Your live `ecommerce.db` instance will never get modified by test tasks.*

### Evaluate Statement & Coverage Reports
Generate a full test statement code coverage dashboard execution footprint:
```bash
pytest --cov=app --cov-report=html -v
```
To visually audit tested statement flows, look up the newly created local directories folder layout and load up **`htmlcov/index.html`** in your preferred local web browser tool.

---

## 🛠️ Continuous Integration (CI)
This repository contains a dedicated **GitHub Actions continuous integration pipeline** (`.github/workflows/ci.yml`). Every time you perform a `git push` or construct a pull request to primary branches, a headless virtual container will automatically spin up, map pip module dependencies cache files, install stack configurations, and evaluate the full testing profile matrix to verify strict stability before deployments.
