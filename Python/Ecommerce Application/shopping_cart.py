# shopping_cart.py
import sqlite3
from database import get_db_connection
from product_catalog import get_product_by_id

def add_to_cart(user_id, product_id, quantity):
    """Add a product to the user's cart"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if product already in cart
    cursor.execute(
        "SELECT id, quantity FROM cart WHERE user_id = ? AND product_id = ?",
        (user_id, product_id)
    )
    existing_item = cursor.fetchone()
    
    if existing_item:
        # Update quantity if product already in cart
        new_quantity = existing_item[1] + quantity
        cursor.execute(
            "UPDATE cart SET quantity = ? WHERE id = ?",
            (new_quantity, existing_item[0])
        )
    else:
        # Add new item to cart
        cursor.execute(
            "INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)",
            (user_id, product_id, quantity)
        )
    
    conn.commit()
    conn.close()
    print("Product added to cart!")

def view_cart(user_id):
    """Display the contents of the user's cart"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT c.id, p.id, p.name, p.price, c.quantity, (p.price * c.quantity) as total
    FROM cart c
    JOIN products p ON c.product_id = p.id
    WHERE c.user_id = ?
    ''', (user_id,))
    
    cart_items = cursor.fetchall()
    conn.close()
    
    print("\n=== Your Shopping Cart ===")
    if not cart_items:
        print("Your cart is empty.")
        return 0
    
    total_amount = 0
    print(f"{'ID':<5} {'Product':<20} {'Price':<10} {'Qty':<5} {'Total'}")
    print("-" * 50)
    for item in cart_items:
        print(f"{item[0]:<5} {item[2]:<20} ${item[3]:<9} {item[4]:<5} ${item[5]:.2f}")
        total_amount += item[5]
    
    print("-" * 50)
    print(f"Total: ${total_amount:.2f}")
    return total_amount

def remove_from_cart(user_id, cart_item_id):
    """Remove an item from the cart"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM cart WHERE id = ? AND user_id = ?",
        (cart_item_id, user_id)
    )
    
    if cursor.rowcount > 0:
        print("Item removed from cart.")
    else:
        print("Item not found in your cart.")
    
    conn.commit()
    conn.close()

def checkout(user_id):
    """Process the checkout and create an order"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # First get the user's email
    cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    user_email = cursor.fetchone()[0]
    
    # Calculate cart total
    cursor.execute('''
    SELECT SUM(p.price * c.quantity) as total
    FROM cart c
    JOIN products p ON c.product_id = p.id
    WHERE c.user_id = ?
    ''', (user_id,))
    
    total_amount = cursor.fetchone()[0] or 0
    
    if total_amount == 0:
        print("Your cart is empty. Add items before checkout.")
        conn.close()
        return False
    
    # Create order
    cursor.execute(
        "INSERT INTO orders (user_id, total_amount) VALUES (?, ?)",
        (user_id, total_amount)
    )
    order_id = cursor.lastrowid
    
    # Move cart items to order items
    cursor.execute('''
    INSERT INTO order_items (order_id, product_id, quantity, price)
    SELECT ?, c.product_id, c.quantity, p.price
    FROM cart c
    JOIN products p ON c.product_id = p.id
    WHERE c.user_id = ?
    ''', (order_id, user_id))
    
    # Update product stock
    cursor.execute('''
    UPDATE products 
    SET stock = stock - c.quantity
    FROM cart c
    WHERE products.id = c.product_id AND c.user_id = ?
    ''', (user_id,))
    
    # Clear cart
    cursor.execute("DELETE FROM cart WHERE user_id = ?", (user_id,))
    
    conn.commit()
    conn.close()
    
    print(f"Order placed successfully! Order ID: {order_id}")
    print(f"Total amount: ${total_amount:.2f}")
    
    # Simulate email confirmation with the actual user email
    print("\n=== Order Confirmation Email ===")
    print(f"To: {user_email}")
    print("Subject: Your Order Confirmation")
    print(f"Thank you for your order! Your order ID is {order_id}.")
    print(f"Total amount: ${total_amount:.2f}")
    print("Your order will be processed shortly.")
    
    return True
