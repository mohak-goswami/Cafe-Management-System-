# Cafe-Management-System
A Python + MySQL-based Cafe Management System designed to simplify everyday café operations. This project automates customer registration, order placement, menu management, and sales reporting, helping cafes improve efficiency and customer experience.

🚀 Features

Admin Functions :-

Secure admin login

Manage customers & orders

Add / update / remove menu items

Generate monthly sales reports

Customer Functions :-

Register & login

Browse menu items

Place orders with UPI payment

⚠️ Disclaimer

This project will not run unless:

MySQL is installed and running on your system.

The database (cafe_central) and tables (customers, menu, orders, order_items) are created exactly as defined in the project SQL scripts.

The MySQL username, password, and host in the code are updated according to your local setup.

🛠️ Tech Stack

Python (for backend logic)

MySQL (for database management)

MySQL Connector for Python


📂 Setup Instructions

Clone this repository:

git clone https://github.com/yourusername/cafe-management-system.git
cd cafe-management-system


Install dependencies:

pip install mysql-connector-python


Create the database and tables in MySQL:

CREATE DATABASE cafe_central;


(Use the SQL table creation scripts provided in the project pdf.)

Run the program:

python Cafe_Central.py

📊 Sample Database Schema

Customers: Stores customer details

Menu: Stores items, categories, and prices

Orders: Records order metadata (customer, date, UPI)

Order_Items: Stores ordered items and quantities

📌 Note

This is a mini-project for learning purposes and is not production-ready. Contributions and improvements are welcomed.
