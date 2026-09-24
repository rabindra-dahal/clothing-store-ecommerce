import sqlite3
from app.config import DB_FILE

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    ''')
    
    # 2. Clothes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clothes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    ''')
    
    # 3. Carts Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS carts (
            username TEXT,
            cloth_id INTEGER,
            quantity INTEGER NOT NULL,
            PRIMARY KEY (username, cloth_id),
            FOREIGN KEY (username) REFERENCES users(username),
            FOREIGN KEY (cloth_id) REFERENCES clothes(id)
        )
    ''')
    
    # 4. Payments Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS payments (
            transaction_id TEXT PRIMARY KEY,
            timestamp TEXT NOT NULL,
            customer TEXT NOT NULL,
            amount_paid REAL NOT NULL,
            card_masked TEXT NOT NULL,
            shopped_items_json TEXT NOT NULL,
            FOREIGN KEY (customer) REFERENCES users(username)
        )
    ''')
    
    # Seed Initial Data if catalog is empty
    cursor.execute("SELECT COUNT(*) FROM clothes")
    if cursor.fetchone()[0] == 0:
        seed_clothes = [
            ("Classic Denim Jacket", "Outerwear", 85.00, 10),
            ("Slim Fit Chino Pants", "Bottoms", 45.50, 15),
            ("Oversized Graphic Tee", "Tops", 28.00, 30),
            ("Floral Summer Dress", "Dresses", 60.00, 8),
            ("Wool Knit Sweater", "Outerwear", 75.00, 5)
        ]
        cursor.executemany(
            "INSERT INTO clothes (name, category, price, stock) VALUES (?, ?, ?, ?)", 
            seed_clothes
        )
        print("Database initialized and seeded with cloth inventory.")
        
    conn.commit()
    conn.close()
