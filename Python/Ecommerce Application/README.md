# Mini Enterprise E-Commerce Application

## Overview
This is a command-line based e-commerce application built with Python and SQLite. It supports two user roles: Customers and Administrators.

## Features Implemented
- User authentication (registration and login) with password hashing
- Product catalog browsing with category filtering
- Shopping cart functionality (add/remove items)
- Order placement and history viewing
- Inventory management (admin only - add/edit/delete products)
- Sales reporting (admin only - revenue, best sellers, category sales)
- Simulated email confirmation after order placement

## How to Run
1. Ensure you have Python 3.x installed
2. Download all the Python files to a directory
3. Navigate to the project directory in your terminal/command prompt
4. Run the application: `python main.py`

## Sample Login Credentials
- Admin: username=`admin`, password=`admin123`
- Customer: Register a new account through the application
- My account: username=`Bider-Man`, password=`Bider-Man`. Use this account to see previous order history, processed payments, etc.

## Database Schema
The application uses SQLite with the following tables:
- users: Stores user credentials and roles
- products: Stores product information
- orders: Stores order headers
- order_items: Stores order details
- cart: Stores temporary cart items

## Modules
- `main.py`: Main application entry point
- `database.py`: Database initialization and connection functions
- `auth.py`: User authentication functions
- `product_catalog.py`: Product browsing functionality
- `shopping_cart.py`: Cart management and checkout
- `order_management.py`: Order history viewing
- `inventory_management.py`: Admin product management
- `sales_report.py`: Admin sales reporting
- `ecommerce.db`: Database containing user information

## Usage Instructions
1. Start the application with `python main.py`
2. Register a new account or login with the admin credentials
3. Browse products and add them to your cart
4. Checkout to place an order
5. Admins can manage inventory and view sales reports

## Bonus Features Implemented
- Category filtering for products
- Simulated email confirmation after order placement
- Detailed sales reports with best sellers and category breakdown
