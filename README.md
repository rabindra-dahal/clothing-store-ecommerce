## Main app folder structure
shopping-sqlite/
│
├── app/
│   ├── __init__.py
│   ├── config.py         # App configurations & secrets
│   ├── database.py       # SQLite connection manager & table creation
│   ├── auth.py           # JWT generation, validation, & password hashing
│   ├── models.py         # Pydantic schemas (Request/Response validation)
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py       # Auth endpoints (signup, login)
│   │   ├── browsing.py   # Public endpoints (clothes catalog)
│   │   └── cart.py       # Protected endpoints (cart, checkout, orders)
│   └── main.py           # FastAPI initialization & router assembly

## Test folder structure

shopping-sqlite/
│
├── app/
│   └── ... above
└── tests/
    ├── __init__.py
    ├── conftest.py      # Fixtures (database reset, test client setup)
    └── test_routes.py   # Test cases for auth, catalog, and checkout

## To see test coverage

```
pip install pytest-cov
pytest --cov=app --cov-report=html -v

pytest -v

```

## Installation 
```
python -m venv venv
pip install -r requirements.txt
```

## Running app
```
uvicorn app.main:app --reload

```