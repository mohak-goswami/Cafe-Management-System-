import mysql.connector
from datetime import datetime
while True:
    try:
        connection = mysql.connector.connect(
            host="localhost",
            database="cafe_central",
            user="root",
            passwd="root"
        )
        if connection.is_connected():
            print("Connected to MySQL database")
    except mysql.connector.Error as e:
        print("Error while connecting to MySQL", e)
        break

    print("\nWelcome to Cafe Management System")
    role = input("Login as (admin/customer) or type 'exit' to quit: ").strip().lower()

    if role == 'admin':
        print("Welcome, Admin!")
        while True:
                print("\nAdmin Menu")
                print("1. View all customers")
                print("2. View all orders")
                print("3. Make changes to the menu")
                print("4. View sales report")
                print("5. Logout")
                choice = input("Select an option: ")

                if choice == '1':
                    cursor = connection.cursor(dictionary=True)
                    cursor.execute("SELECT * FROM customers")
                    customers = cursor.fetchall()
                    cursor.close()

                    print("\n--- Customers ---")
                    for customer in customers:
                        print(f"ID: {customer['id']}, Name: {customer['name']}, Email: {customer['email']}, Phone: {customer['phone']}")
                    print("----------------")

                elif choice == '2':
                    cursor = connection.cursor(dictionary=True)
                    cursor.execute("SELECT * FROM orders")
                    orders = cursor.fetchall()
                    cursor.close()

                    print("\n--- Orders ---")
                    for order in orders:
                        print(f"Order ID: {order['id']}, Customer ID: {order['customer_id']}, Date: {order['date']}, UPI: {order['upi_number']}")
                    print("----------------")

                elif choice == '3':
                    while True:
                        # Display the current menu
                        print("\n--- Current Menu ---")
                        cursor = connection.cursor(dictionary=True)
                        cursor.execute("SELECT * FROM menu")
                        menu_items = cursor.fetchall()
                        cursor.close()

                        for item in menu_items:
                            print(f"{item['id']}. {item['category']} - {item['name']} - ${item['price']}")
                        print("---------------------\n")

                        # Show menu modification options
                        print("Menu Modification Options:")
                        print("1. Add a menu item")
                        print("2. Remove a menu item")
                        print("3. Change details of a menu item")
                        print("4. Go back to Admin Menu")

                        submenu_choice = input("Select an option: ")

                        if submenu_choice == '1':
                            name = input("Enter item name: ")
                            category = input("Enter category: ")
                            price = float(input("Enter price: "))

                            cursor = connection.cursor()
                            cursor.execute("INSERT INTO menu (name, category, price) VALUES (%s, %s, %s)", (name, category, price))
                            connection.commit()
                            cursor.close()
                            print("Menu item added successfully!")

                        elif submenu_choice == '2':
                            try:
                                item_id = int(input("Enter the ID of the item to remove: "))
                                cursor = connection.cursor()
                                cursor.execute("DELETE FROM menu WHERE id = %s", (item_id,))
                                connection.commit()
                                cursor.close()
                                print("Menu item removed successfully!")
                            except ValueError:
                                print("Invalid ID. Please enter a number.")

                        elif submenu_choice == '3':
                            try:
                                item_id = int(input("Enter the ID of the item to modify: "))
                                cursor = connection.cursor(dictionary=True)
                                cursor.execute("SELECT * FROM menu WHERE id = %s", (item_id,))
                                item = cursor.fetchone()
                                cursor.close()

                                if item:
                                    print(f"Current Details: {item['name']} - {item['category']} - ${item['price']}")
                                    new_name = input(f"Enter new name (leave blank to keep '{item['name']}'): ") or item['name']
                                    new_category = input(f"Enter new category (leave blank to keep '{item['category']}'): ") or item['category']
                                    new_price = input(f"Enter new price (leave blank to keep '${item['price']}'): ")
                                    new_price = float(new_price) if new_price else item['price']

                                    cursor = connection.cursor()
                                    cursor.execute(
                                        "UPDATE menu SET name = %s, category = %s, price = %s WHERE id = %s",
                                        (new_name, new_category, new_price, item_id)
                                    )
                                    connection.commit()
                                    cursor.close()
                                    print("Menu item updated successfully!")
                                else:
                                    print("Item not found.")
                            except ValueError:
                                print("Invalid ID. Please enter a number.")

                        elif submenu_choice == '4':
                            print("Returning to Admin Menu.")
                            break
                        else:
                            print("Invalid option. Please try again.")

                elif choice == '4':
                    cursor = connection.cursor(dictionary=True)
                    cursor.execute("""
                        SELECT 
                            MONTH(o.date) AS month, 
                            SUM(oi.total_price) AS total_sales
                        FROM 
                            order_items oi
                        JOIN 
                            orders o ON oi.order_id = o.id
                        GROUP BY 
                            MONTH(o.date)
                    """)
                    sales_report = cursor.fetchall()
                    cursor.close()

                    print("\n--- Monthly Sales Report ---")
                    for report in sales_report:
                        print(f"Month: {report['month']}, Total Sales: ${report['total_sales']}")
                    print("----------------------------\n")

                elif choice == '5':
                    print("Logging out of Admin menu.")
                    break
                else:
                    print("Invalid option")

    elif role == 'customer':
        first_time = input("Is this your first time? (yes/no): ").strip().lower()
        if first_time == 'yes':
            name = input("Enter your name: ")
            phone = input("Enter your phone number: ")
            email = input("Enter your email: ")
            cursor = connection.cursor()
            cursor.execute("INSERT INTO customers (name, phone, email) VALUES (%s, %s, %s)", (name, phone, email))
            connection.commit()
            customer_id = cursor.lastrowid
            cursor.close()
            print(f"Registration successful! Your customer ID is {customer_id}")

        customer_id = input("Enter your customer ID: ")
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        cursor.close()

        if customer:
            print(f"Welcome back, {customer['name']}!")
            while True:
                # Display menu
                print("\nCustomer Menu")
                print("1. View Menu")
                print("2. Place Order")
                print("3. Logout")
                choice = input("Select an option: ")

                if choice == '1':
                    cursor = connection.cursor(dictionary=True)
                    cursor.execute("SELECT * FROM menu")
                    menu_items = cursor.fetchall()
                    cursor.close()

                    print("\n--- Menu ---")
                    for item in menu_items:
                        print(f"{item['id']}. {item['category']} - {item['name']} - ${item['price']}")
                    print("----------------\n")

                elif choice == '2':
                    cursor = connection.cursor(dictionary=True)
                    cursor.execute("SELECT * FROM menu")
                    menu_items = cursor.fetchall()
                    cursor.close()

                    order_items = []
                    while True:
                        item_id = input("Enter the item ID to order (or type 'done' to finish): ")
                        if item_id.lower() == 'done':
                            break
                        try:
                            item_id = int(item_id)
                            quantity = int(input("Enter quantity: "))
                            selected_item = next((item for item in menu_items if item['id'] == item_id), None)
                            if selected_item:
                                order_items.append((item_id, quantity, selected_item['price'] * quantity))
                            else:
                                print("Invalid item ID.")
                        except ValueError:
                            print("Please enter valid numbers.")

                    if not order_items:
                        print("No items ordered.")
                    else:
                        upi_number = input("Enter your UPI number for payment: ")

                        # Insert order details into the database
                        cursor = connection.cursor()
                        cursor.execute("INSERT INTO orders (customer_id, date, upi_number) VALUES (%s, %s, %s)", 
                                       (customer_id, datetime.now(), upi_number))
                        order_id = cursor.lastrowid
                        for item_id, quantity, total_price in order_items:
                            cursor.execute("INSERT INTO order_items (order_id, item_id, quantity, total_price) VALUES (%s, %s, %s, %s)",
                                           (order_id, item_id, quantity, total_price))
                        connection.commit()
                        cursor.close()
                        print(f"Order placed successfully! Your order ID is {order_id}.")
                elif choice == '3':
                    print("Logging out of Customer menu.")
                    break
                else:
                    print("Invalid option.")
        else:
            print("Invalid customer ID")

    elif role == 'exit':
        print("Thank you for using Cafe Management System.")
        break
    else:
        print("Invalid role. Please try again.")


'''
-- Create the cafe database
CREATE DATABASE cafe_central;

-- Create the `customers` table
CREATE TABLE customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

-- Create the `menu` table
CREATE TABLE menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL);

-- Create the `orders` table
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    date DATETIME DEFAULT CURRENT_TIMESTAMP,
    upi_number VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(id) ON DELETE CASCADE);

-- Create the `order_items` table
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES menu(id) ON DELETE CASCADE);
'''
