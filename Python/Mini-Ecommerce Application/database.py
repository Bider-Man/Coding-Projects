# database.py
import sqlite3
import hashlib

def create_tables():
    """Initialize database tables if they don't exist"""
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL DEFAULT 'customer',
        email TEXT NOT NULL
    )
    ''')
    
    # Products table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        category TEXT NOT NULL,
        stock INTEGER NOT NULL,
        description TEXT
    )
    ''')
    
    # Orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        total_amount REAL NOT NULL,
        status TEXT DEFAULT 'Processing',
        FOREIGN KEY (user_id) REFERENCES users (id)
    )
    ''')
    
    # Order items table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS order_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        FOREIGN KEY (order_id) REFERENCES orders (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')
    
    # Cart table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    ''')
    
    # Create default admin user if not exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='admin'")
    if cursor.fetchone()[0] == 0:
        hashed_password = hash_password("admin123")
        cursor.execute(
            "INSERT INTO users (username, password, role, email) VALUES (?, ?, ?, ?)",
            ("admin", hashed_password, "admin", "admin@example.com")
        )
        print("Default admin user created: username=admin, password=admin123")
    
    # Add some sample products if none exist
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        sample_products = [
            ("Laptop", 999.99, "Electronics", 10, "High-performance laptop with 16GB RAM"),
            ("Smartphone", 499.99, "Electronics", 15, "Latest smartphone with great camera"),
            ("T-Shirt", 19.99, "Clothing", 50, "Cotton t-shirt in various colors"),
            ("Coffee Mug", 9.99, "Home", 30, "Ceramic mug with handle"),
            ("Book", 14.99, "Education", 25, "Bestselling novel"),
            ("Headphones", 79.99, "Electronics", 12, "Noise-cancelling headphones")
        ]
        cursor.executemany(
            "INSERT INTO products (name, price, category, stock, description) VALUES (?, ?, ?, ?, ?)",
            sample_products
        )
        print("Sample products added to inventory.")
    
    conn.commit()
    conn.close()

def get_db_connection():
    """Get a database connection"""
    return sqlite3.connect('ecommerce.db')

def hash_password(password):
    """Hash a password for security"""
    return hashlib.sha256(password.encode()).hexdigest()
