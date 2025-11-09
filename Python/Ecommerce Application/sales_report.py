# sales_report.py
import sqlite3
from database import get_db_connection

def view_sales_report():
    """Generate and display sales reports"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Total revenue
    cursor.execute("SELECT SUM(total_amount) FROM orders")
    total_revenue = cursor.fetchone()[0] or 0
    
    # Total orders
    cursor.execute("SELECT COUNT(*) FROM orders")
    total_orders = cursor.fetchone()[0]
    
    # Best selling products
    cursor.execute('''
    SELECT p.name, SUM(oi.quantity) as total_sold, SUM(oi.quantity * oi.price) as revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    GROUP BY p.id
    ORDER BY total_sold DESC
    LIMIT 5
    ''')
    best_sellers = cursor.fetchall()
    
    # Sales by category
    cursor.execute('''
    SELECT p.category, SUM(oi.quantity) as total_sold, SUM(oi.quantity * oi.price) as revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.id
    GROUP BY p.category
    ORDER BY revenue DESC
    ''')
    category_sales = cursor.fetchall()
    
    conn.close()
    
    print("\n=== Sales Report ===")
    print(f"Total Revenue: ${total_revenue:.2f}")
    print(f"Total Orders: {total_orders}")
    
    print("\n=== Top 5 Best Sellers ===")
    print(f"{'Product':<20} {'Units Sold':<12} {'Revenue'}")
    print("-" * 40)
    for product in best_sellers:
        print(f"{product[0]:<20} {product[1]:<12} ${product[2]:.2f}")
    
    print("\n=== Sales by Category ===")
    print(f"{'Category':<15} {'Units Sold':<12} {'Revenue'}")
    print("-" * 40)
    for category in category_sales:
        print(f"{category[0]:<15} {category[1]:<12} ${category[2]:.2f}")
