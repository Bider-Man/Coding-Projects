# auth.py
import sqlite3
import getpass  # Add this import
from database import get_db_connection, hash_password

def register_user():
    """Register a new user"""
    print("\n=== User Registration ===")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")  # Changed to getpass
    email = input("Enter email: ")
    
    if not username or not password or not email:
        print("All fields are required.")
        return False
    
    hashed_password = hash_password(password)
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password, email) VALUES (?, ?, ?)",
            (username, hashed_password, email)
        )
        conn.commit()
        conn.close()
        print("Registration successful! You can now login.")
        return True
    except sqlite3.IntegrityError:
        print("Username already exists. Please choose a different username.")
        return False

def login_user():
    """Login a user and return user info if successful"""
    print("\n=== User Login ===")
    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")  # Changed to getpass
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, password, role, email FROM users WHERE username = ?",  # Added email to SELECT
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    
    if user and user[2] == hash_password(password):
        print(f"Login successful! Welcome {username}.")
        return {
            'id': user[0],
            'username': user[1],
            'role': user[3],
            'email': user[4]  # Added email to returned user data
        }
    else:
        print("Invalid username or password.")
        return None
