# inventory_management.py
import sqlite3
import re
from database import get_db_connection

def clean_price_input(price_str):
    """Remove any non-numeric characters from price input except decimal point"""
    # Remove any currency symbols, commas, etc.
    cleaned = re.sub(r'[^\d.]', '', price_str)
    try:
        return float(cleaned)
    except ValueError:
        return 0.0

def view_all_products():
    """Display all products with details"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, category, stock, description FROM products")
    products = cursor.fetchall()
    conn.close()
    
    print("\n=== All Products ===")
    print(f"{'ID':<5} {'Name':<20} {'Price':<10} {'Category':<15} {'Stock':<10} {'Description'}")
    print("-" * 80)
    for product in products:
        print(f"{product[0]:<5} {product[1]:<20} ${product[2]:<9.2f} {product[3]:<15} {product[4]:<10} {product[5]}")

def add_product():
    """Add a new product to inventory"""
    print("\n=== Add New Product ===")
    name = input("Product name: ")
    price_input = input("Price: ")
    price = clean_price_input(price_input)
    category = input("Category: ")
    stock = int(input("Stock: "))
    description = input("Description: ")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO products (name, price, category, stock, description) VALUES (?, ?, ?, ?, ?)",
        (name, price, category, stock, description)
    )
    conn.commit()
    conn.close()
    
    print("Product added successfully!")

def update_product():
    """Update an existing product"""
    product_id = input("Enter product ID to update: ")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, name, price, category, stock, description FROM products WHERE id = ?",
        (product_id,)
    )
    product = cursor.fetchone()
    
    if not product:
        print("Product not found.")
        conn.close()
        return
    
    print(f"\nUpdating product: {product[1]}")
    name = input(f"Name ({product[1]}): ") or product[1]
    
    price_input = input(f"Price (${product[2]}): ") or str(product[2])
    price = clean_price_input(price_input)
    
    category = input(f"Category ({product[3]}): ") or product[3]
    stock_input = input(f"Stock ({product[4]}): ") or str(product[4])
    stock = int(stock_input) if stock_input.isdigit() else product[4]
    description = input(f"Description ({product[5]}): ") or product[5]
    
    cursor.execute(
        "UPDATE products SET name = ?, price = ?, category = ?, stock = ?, description = ? WHERE id = ?",
        (name, price, category, stock, description, product_id)
    )
    conn.commit()
    conn.close()
    
    print("Product updated successfully!")

def delete_product():
    """Delete a product from inventory"""
    product_id = input("Enter product ID to delete: ")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if product exists
    cursor.execute("SELECT name FROM products WHERE id = ?", (product_id,))
    product = cursor.fetchone()
    
    if not product:
        print("Product not found.")
        conn.close()
        return
    
    # Confirm deletion
    confirm = input(f"Are you sure you want to delete '{product[0]}'? (y/n): ")
    if confirm.lower() == 'y':
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        print("Product deleted successfully!")
    else:
        print("Deletion cancelled.")
    
    conn.close()

def manage_inventory():
    """Admin interface for inventory management"""
    while True:
        print("\n=== Inventory Management ===")
        print("1. View all products")
        print("2. Add new product")
        print("3. Update product")
        print("4. Delete product")
        print("5. Back to admin menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            view_all_products()
        elif choice == "2":
            add_product()
        elif choice == "3":
            update_product()
        elif choice == "4":
            delete_product()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")
