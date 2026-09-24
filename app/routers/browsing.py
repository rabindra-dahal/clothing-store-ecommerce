from typing import Optional
from fastapi import APIRouter, HTTPException
from app.database import get_db_connection

router = APIRouter(prefix="/clothes", tags=["Browsing"])

@router.get("")
def browse_clothes(category: Optional[str] = None):
    """Browse clothing items freely from SQLite without needing authentication."""
    conn = get_db_connection()
    if category:
        rows = conn.execute("SELECT * FROM clothes WHERE LOWER(category) = LOWER(?)", (category,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM clothes").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.get("/{cloth_id}")
def get_cloth_details(cloth_id: int):
    """View details of a specific clothing item from DB."""
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM clothes WHERE id = ?", (cloth_id,)).fetchone()
    conn.close()
    if row is None:
        raise HTTPException(status_code=404, detail="Clothing item not found")
    return dict(row)
