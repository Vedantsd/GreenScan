import sqlite3


DB_NAME = "greenscan.db"

# ---------- Create products table ----------
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    decomposability_status TEXT NOT NULL,
    decomposability_percent INTEGER,
    decomposition_years INTEGER
)""")
conn.commit()
conn.close()


def add_product(name, status, percent, years):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO products (name, decomposability_status, decomposability_percent, decomposition_years)
    VALUES (?, ?, ?, ?)
    """, (name, status, percent, years))

    product_id = cursor.lastrowid
    conn.commit()
    conn.close()
    print(f"✅ Product '{name}' added successfully!")
    
    return product_id


def get_report_data(product_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM products WHERE product_id = ?", (product_id,))
    row = cursor.fetchone()

    conn.close()
    return dict(row) if row else None
