import sqlite3
import csv
import os

# Paths
csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../csv"))
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../db/lesson.db"))

# Delete old DB
if os.path.exists(db_path):
    os.remove(db_path)

# Connect
conn = sqlite3.connect(db_path)
cur = conn.cursor()
conn.execute("PRAGMA foreign_keys = 1")  # enable foreign keys

# Create tables
cur.execute("""
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    date TEXT,
    customer_id INTEGER,
    employee_id INTEGER
)
""")

cur.execute("""
CREATE TABLE line_items (
    line_item_id INTEGER PRIMARY KEY,
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER
)
""")

cur.execute("""
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    price REAL
)
""")

cur.execute("""
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT,
    contact TEXT,
    street TEXT,
    city TEXT,
    country TEXT,
    postal_code TEXT,
    phone TEXT
)
""")

cur.execute("""
CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    phone TEXT
)
""")

# Function to load CSV into table
def load_csv(table, file_name):
    file_path = os.path.join(csv_path, file_name)
    with open(file_path, "r") as f:
        dr = csv.DictReader(f)
        columns = dr.fieldnames
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?']*len(columns))})"
        for row in dr:
            cur.execute(query, [row[col] for col in columns])

# Load CSVs
load_csv("orders", "orders.csv")
load_csv("line_items", "line_items.csv")
load_csv("products", "products.csv")
load_csv("customers", "customers.csv")
load_csv("employees", "employees.csv")

conn.commit()

# Task 1: Total price of first 5 orders
query1 = """
SELECT o.order_id,
       SUM(p.price * li.quantity) AS total_price
FROM orders o
JOIN line_items li ON o.order_id = li.order_id
JOIN products p ON li.product_id = p.product_id
GROUP BY o.order_id
ORDER BY o.order_id
LIMIT 5;
"""
cur.execute(query1)
results1 = cur.fetchall()

print("Task 1: Order ID | Total Price")
print("-----------------------------")
for row in results1:
    print(f"{row[0]} | {row[1]:.2f}")

# Task 2: Average order price per customer
query2 = """
SELECT c.customer_name,
       AVG(sub.total_price) AS average_total_price
FROM customers c
LEFT JOIN (
    SELECT li.order_id,
           o.customer_id AS customer_id_b,
           SUM(li.quantity * p.price) AS total_price
    FROM orders o
    JOIN line_items li ON o.order_id = li.order_id
    JOIN products p ON li.product_id = p.product_id
    GROUP BY li.order_id
) AS sub
ON c.customer_id = sub.customer_id_b
GROUP BY c.customer_id
ORDER BY c.customer_id;
"""
cur.execute(query2)
results2 = cur.fetchall()

print("\nTask 2: Customer Name | Average Total Price")
print("-------------------------------------------")
for row in results2:
    avg_price = row[1] if row[1] is not None else 0
    print(f"{row[0]} | {avg_price:.2f}")

# Task 3: Insert a new order for Perez and Sons
# Get IDs
cur.execute("SELECT customer_id FROM customers WHERE customer_name = ?", ("Perez and Sons",))
customer_id = cur.fetchone()[0]

cur.execute("SELECT employee_id FROM employees WHERE first_name = ? AND last_name = ?", ("Miranda", "Harris"))
employee_id = cur.fetchone()[0]

cur.execute("SELECT product_id FROM products ORDER BY price ASC LIMIT 5")
product_ids = [row[0] for row in cur.fetchall()]

# Transaction to insert order + line_items
with conn:
    cur.execute(
        "INSERT INTO orders (customer_id, employee_id, date) VALUES (?, ?, DATE('now')) RETURNING order_id",
        (customer_id, employee_id)
    )
    order_id = cur.fetchone()[0]

    for pid in product_ids:
        cur.execute(
            "INSERT INTO line_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
            (order_id, pid, 10)
        )

# Print line items with product names
cur.execute("""
SELECT li.line_item_id, li.quantity, p.product_name
FROM line_items li
JOIN products p ON li.product_id = p.product_id
WHERE li.order_id = ?
""", (order_id,))
line_items = cur.fetchall()

print("\nTask 3: New Order Line Items")
print("---------------------------")
for row in line_items:
    print(f"Line Item ID: {row[0]}, Quantity: {row[1]}, Product: {row[2]}")

# Task 4: Employees with more than 5 orders
query4 = """
SELECT e.employee_id, e.first_name, e.last_name, COUNT(o.order_id) AS order_count
FROM employees e
JOIN orders o ON e.employee_id = o.employee_id
GROUP BY e.employee_id
HAVING COUNT(o.order_id) > 5
ORDER BY order_count DESC;
"""
cur.execute(query4)
results4 = cur.fetchall()

print("\nTask 4: Employees with More Than 5 Orders")
print("------------------------------------------")
for row in results4:
    print(f"Employee ID: {row[0]}, Name: {row[1]} {row[2]}, Orders: {row[3]}")

# Close connection
conn.close()
