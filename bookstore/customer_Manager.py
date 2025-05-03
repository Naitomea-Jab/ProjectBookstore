# customer_Manager.py
import sqlite3
from bookstore.utilities import DB_PATH

def get_customers():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer;")
    data = cursor.fetchall()
    conn.close()
    return data
