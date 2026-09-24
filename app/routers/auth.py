import sqlite3
from fastapi import APIRouter, HTTPException
from app.models import UserAuth
from app.database import get_db_connection
from app.auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=201)
def signup(user: UserAuth):
    """Register a new customer account securely in SQLite."""
    conn = get_db_connection()
    existing_user = conn.execute("SELECT username FROM users WHERE username = ?", (user.username,)).fetchone()
    
    if existing_user:
        conn.close()
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_pwd = hash_password(user.password)

    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user.username, hashed_pwd))
        conn.commit()
    except sqlite3.Error:
        raise HTTPException(status_code=500, detail="Database write failure.")
    finally:
        conn.close()
        
    return {"message": "User registered successfully"}

@router.post("/login")
def login(user: UserAuth):
    """Authenticate credentials against database records and obtain a bearer access token."""
    conn = get_db_connection()
    db_user = conn.execute("SELECT * FROM users WHERE username = ?", (user.username,)).fetchone()
    conn.close()
    
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    token = create_access_token(data={"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
