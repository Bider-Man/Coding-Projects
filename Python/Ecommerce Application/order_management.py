# order_management.py
import sqlite3
from database import get_db_connection

def view_order_history(user_id):
    """Display order history for a user"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT o.id, o.order_date, o.total_amount, o.status
    FROM orders o
    WHERE o.user_id = ?
    ORDER BY o.order_date DESC
    ''', (user_id,))
    
    orders = cursor.fetchall()
    
    print("\n=== Your Order History ===")
    if not orders:
        print("You have no orders yet.")
        conn.close()
        return
    
    print(f"{'Order ID':<10} {'Date':<20} {'Amount':<10} {'Status'}")
    print("-" * 50)
    for order in orders:
        print(f"{order[0]:<10} {order[1]:<20} ${order[2]:<9} {order[3]}")
    
    # Allow viewing order details
    order_id = input("\nEnter Order ID to view details (or press Enter to go back): ")
    if order_id:
        view_order_details(order_id, user_id)
    
    conn.close()

def view_order_details(order_id, user_id):
    """Display details of a specific order"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Verify the order belongs to the user
    cursor.execute(
        "SELECT id FROM orders WHERE id = ? AND user_id = ?",
        (order_id, user_id)
    )
    
    if not cursor.fetchone():
        print("Order not found or you don't have permission to view it.")
        conn.close()
        return
    
    # Get order items
    cursor.execute('''
    SELECT p.name, oi.quantity, oi.price, (oi.quantity * oi.price) as total
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    WHERE oi.order_id = ?
    ''', (order_id,))
    
    items = cursor.fetchall()
    
    print(f"\n=== Order #{order_id} Details ===")
    print(f"{'Product':<20} {'Qty':<5} {'Price':<10} {'Total'}")
    print("-" * 45)
    for item in items:
        print(f"{item[0]:<20} {item[1]:<5} ${item[2]:<9} ${item[3]:.2f}")
    
    conn.close()

def view_all_orders():
    """Admin function to view all orders"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT o.id, u.username, o.order_date, o.total_amount, o.status
    FROM orders o
    JOIN users u ON o.user_id = u.id
    ORDER BY o.order_date DESC
    ''')
    
    orders = cursor.fetchall()
    
    print("\n=== All Orders ===")
    print(f"{'Order ID':<10} {'Customer':<15} {'Date':<20} {'Amount':<10} {'Status'}")
    print("-" * 65)
    for order in orders:
        print(f"{order[0]:<10} {order[1]:<15} {order[2]:<20} ${order[3]:<9} {order[4]}")
    
    conn.close()
