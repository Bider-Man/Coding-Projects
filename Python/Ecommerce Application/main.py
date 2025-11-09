# main.py
from database import create_tables
from auth import register_user, login_user
from product_catalog import display_products, get_categories, get_product_by_id
from shopping_cart import add_to_cart, view_cart, remove_from_cart, checkout
from order_management import view_order_history, view_all_orders
from inventory_management import manage_inventory
from sales_report import view_sales_report

def handle_cart_operations(user_id):
    """Handle cart operations after adding items"""
    while True:
        print("\n1. Continue shopping")
        print("2. View cart")
        print("3. Checkout")
        print("4. Back to main menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1":
            return "continue_shopping"
        elif choice == "2":
            total = view_cart(user_id)
            if total > 0:
                print("\n1. Checkout")
                print("2. Remove item")
                print("3. Continue shopping")
                
                cart_choice = input("Enter your choice: ")
                
                if cart_choice == "1":
                    checkout(user_id)
                    return "main_menu"
                elif cart_choice == "2":
                    try:
                        item_id = int(input("Enter cart item ID to remove: "))
                        remove_from_cart(user_id, item_id)
                    except ValueError:
                        print("Invalid input.")
            return "continue_shopping"
        elif choice == "3":
            checkout(user_id)
            return "main_menu"
        elif choice == "4":
            return "main_menu"
        else:
            print("Invalid choice. Please try again.")

def main():
    # Initialize database
    create_tables()
    
    current_user = None
    
    while True:
        if current_user is None:
            # Not logged in
            print("\n=== Mini E-Commerce Application ===")
            print("1. Register")
            print("2. Login")
            print("3. Browse Products")
            print("4. Exit")
            
            choice = input("Enter your choice: ")
            
            if choice == "1":
                register_user()
            elif choice == "2":
                current_user = login_user()
            elif choice == "3":
                display_products()
            elif choice == "4":
                print("Thank you for using our application!")
                break
            else:
                print("Invalid choice. Please try again.")
        else:
            # Logged in
            if current_user['role'] == "customer":
                print(f"\n=== Customer Dashboard (Welcome {current_user['username']}) ===")
                print("1. Browse Products")
                print("2. View Cart")
                print("3. Checkout")
                print("4. View Order History")
                print("5. Logout")
                
                choice = input("Enter your choice: ")
                
                if choice == "1":
                    continue_shopping = True
                    while continue_shopping:
                        categories = get_categories()
                        print("\nCategories:", ", ".join(categories))
                        category_filter = input("Enter category to filter (or press Enter for all): ")
                        products = display_products(category_filter if category_filter else None)
                        
                        if products:
                            try:
                                product_id = int(input("Enter product ID to add to cart (or 0 to go back): "))
                                if product_id == 0:
                                    continue_shopping = False
                                elif product_id > 0:
                                    quantity = int(input("Enter quantity: "))
                                    add_to_cart(current_user['id'], product_id, quantity)
                                    
                                    # After adding to cart, offer options
                                    next_action = handle_cart_operations(current_user['id'])
                                    if next_action == "main_menu":
                                        continue_shopping = False
                            except ValueError:
                                print("Invalid input.")
                        else:
                            continue_shopping = False
                
                elif choice == "2":
                    total = view_cart(current_user['id'])
                    if total > 0:
                        print("\n1. Checkout")
                        print("2. Remove item")
                        print("3. Continue shopping")
                        
                        cart_choice = input("Enter your choice: ")
                        
                        if cart_choice == "1":
                            checkout(current_user['id'])
                        elif cart_choice == "2":
                            try:
                                item_id = int(input("Enter cart item ID to remove: "))
                                remove_from_cart(current_user['id'], item_id)
                            except ValueError:
                                print("Invalid input.")
                
                elif choice == "3":
                    checkout(current_user['id'])
                
                elif choice == "4":
                    view_order_history(current_user['id'])
                
                elif choice == "5":
                    current_user = None
                    print("Logged out successfully.")
                
                else:
                    print("Invalid choice. Please try again.")
                    
            elif current_user['role'] == "admin":
                print(f"\n=== Admin Dashboard (Welcome {current_user['username']}) ===")
                print("1. Manage Inventory")
                print("2. View Sales Report")
                print("3. View All Orders")
                print("4. Logout")
                
                choice = input("Enter your choice: ")
                
                if choice == "1":
                    manage_inventory()
                elif choice == "2":
                    view_sales_report()
                elif choice == "3":
                    view_all_orders()
                elif choice == "4":
                    current_user = None
                    print("Logged out successfully.")
                else:
                    print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
