import sqlite3

def connect_db():
    return sqlite3.connect("restaurant.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS menu (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            price REAL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item TEXT,
            quantity INTEGER,
            total REAL
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM menu")
    if cursor.fetchone()[0] == 0:
        default_items = [
            ("Paneer Tikka", "Starter", 180),
            ("Veg Biryani", "Main Course", 240),
            ("Gulab Jamun", "Dessert", 80),
            ("Lassi", "Beverage", 60),
            ("Butter Naan", "Main Course", 40),
            ("Cold Coffee", "Beverage", 70),
            ("Tomato Soup", "Starter", 90),
            ("Chilli Paneer", "Starter", 150),
            ("Tandoori Roti", "Main Course", 20),
            ("Jeera Rice", "Main Course", 120),
            ("Matar Paneer", "Main Course", 210),
            ("Aloo Gobi", "Main Course", 180),
            ("Chocolate Brownie", "Dessert", 100),
            ("Vanilla Ice Cream", "Dessert", 60),
            ("Mango Shake", "Beverage", 80),
            ("Masala Chai", "Beverage", 30),
            ("Veg Manchurian", "Starter", 160),
            ("Fried Rice", "Main Course", 130),
            ("Dal Makhani", "Main Course", 200),
            ("Rasgulla", "Dessert", 90),
            ("Samosa", "Starter", 30),
            ("Spring Roll", "Starter", 100),
            ("Rajma Chawal", "Main Course", 150),
            ("Coca-Cola", "Beverage", 40),
            ("Sweet Lassi", "Beverage", 65),
            ("Shahi Paneer", "Main Course", 230),
        ]
        cursor.executemany("INSERT INTO menu (name, category, price) VALUES (?, ?, ?)", default_items)

    conn.commit()
    conn.close()

def add_menu_item(name, category, price):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO menu (name, category, price) VALUES (?, ?, ?)", (name, category, price))
    conn.commit()
    conn.close()

def get_menu():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    items = cursor.fetchall()
    conn.close()
    return items

def delete_menu_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM menu WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def place_order(item, quantity, total):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (item, quantity, total) VALUES (?, ?, ?)", (item, quantity, total))
    conn.commit()
    conn.close()

def get_orders():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    conn.close()
    return orders
