import os

SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_clothing_store_key_change_this_in_production")
ALGORITHM = "HS256"
DB_FILE = os.getenv("DB_FILE", "ecommerce.db")
ACCESS_TOKEN_EXPIRE_HOURS = 2
