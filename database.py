import sqlite3

conn = sqlite3.connect("database.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
price INTEGER,
image TEXT
)
""")

cur.execute("DELETE FROM products")

products = [
("Rice", 50, "rice.jpg"),
("Wheat Flour", 45, "wheat.jpg"),
("Sugar", 40, "sugar.jpg"),
("Salt", 20, "salt.jpg"),
("Milk", 40, "milk.jpg"),
("Bread", 30, "bread.jpg"),
("Eggs", 70, "eggs.jpg"),
("Apple", 120, "apple.jpg"),
("Banana", 60, "banana.jpg"),
("Tomato", 35, "tomato.jpg"),
("Potato", 30, "potato.jpg"),
("Onion", 40, "onion.jpg"),
("Cooking Oil", 150, "oil.jpg"),
("Tea Powder", 90, "tea.jpg"),
("Coffee Powder", 120, "coffee.jpg")
]

cur.executemany("INSERT INTO products (name,price,image) VALUES (?,?,?)", products)

conn.commit()
conn.close()

print("15 Grocery Products Added Successfully")