import sqlite3
import random
from faker import Faker

fake = Faker()

conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# -----------------------------
# Create Tables
# -----------------------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    department TEXT,
    salary INTEGER,
    city TEXT,
    hire_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    category TEXT,
    price REAL,
    stock INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Orders(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    order_date TEXT,
    FOREIGN KEY(employee_id) REFERENCES Employees(id),
    FOREIGN KEY(product_id) REFERENCES Products(id)
)
""")

# -----------------------------
# Fake Data
# -----------------------------

departments = [
    "IT",
    "Sales",
    "HR",
    "Finance",
    "Marketing"
]

categories = [
    "Laptop",
    "Phone",
    "Monitor",
    "Keyboard",
    "Mouse",
    "Printer",
    "Accessory"
]

# -----------------------------
# Employees
# -----------------------------

for _ in range(50):
    cursor.execute("""
    INSERT INTO Employees
    (first_name,last_name,department,salary,city,hire_date)
    VALUES (?,?,?,?,?,?)
    """,(
        fake.first_name(),
        fake.last_name(),
        random.choice(departments),
        random.randint(30000,120000),
        fake.city(),
        fake.date_between(
            start_date="-8y",
            end_date="today"
        ).isoformat()
    ))

# -----------------------------
# Products
# -----------------------------

for _ in range(100):
    cursor.execute("""
    INSERT INTO Products
    (name,category,price,stock)
    VALUES (?,?,?,?)
    """,(
        fake.word().capitalize(),
        random.choice(categories),
        round(random.uniform(20,5000),2),
        random.randint(0,300)
    ))

# -----------------------------
# Orders
# -----------------------------

for _ in range(1000):
    cursor.execute("""
    INSERT INTO Orders
    (employee_id,product_id,quantity,order_date)
    VALUES (?,?,?,?)
    """,(
        random.randint(1,50),
        random.randint(1,100),
        random.randint(1,10),
        fake.date_between(
            start_date="-2y",
            end_date="today"
        ).isoformat()
    ))

conn.commit()
conn.close()

print("company.db created successfully.")