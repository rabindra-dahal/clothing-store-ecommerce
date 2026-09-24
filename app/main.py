from fastapi import FastAPI
from app.database import init_db
from app.routers import auth, browsing, cart

app = FastAPI(
    title="Threads & Trends API",
    description="Cloth Shopping E-Commerce Backend (Modular Architecture)",
    version="3.0.0"
)

# Trigger Database Setup & Initial Seeding on startup
init_db()

# Assemble Routers
app.include_router(auth.router)
app.include_router(browsing.router)
app.include_router(cart.router)
