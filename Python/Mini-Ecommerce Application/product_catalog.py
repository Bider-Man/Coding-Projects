# product_catalog.py
import sqlite3
from database import get_db_connection

def display_products(category_filter=None):
    """Display all products with optional category filter"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if category_filter:
        cursor.execute(
            "SELECT id, name, price, category, stock, description FROM products WHERE category = ?",
            (category_filter,)
        )
    else:
        cursor.execute("SELECT id, name, price, category, stock, description FROM products")
    
    products = cursor.fetchall()
    conn.close()
    
    print("\n=== Product Catalog ===")
    if not products:
        print("No products found.")
        return
    
    print(f"{'ID':<5} {'Name':<20} {'Price':<10} {'Category':<15} {'Stock':<10} {'Description'}")
    print("-" * 80)
    for product in products:
        print(f"{product[0]:<5} {product[1]:<20} ${product[2]:<9} {product[3]:<15} {product[4]:<10} {product[5]}")
    
    return products

def get_categories():
    """Get all available product categories"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products")
    categories = [row[0] for row in cursor.fetchall()]
    conn.close()
    return categories

def get_product_by_id(product_id):
    """Get product details by ID"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, price, category, stock FROM products WHERE id = ?",
        (product_id,)
    )
    product = cursor.fetchone()
    conn.close()
    return product
