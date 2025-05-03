# customerManager.py
import sqlite3
from bookstore.utilities import DB_PATH

def getCustomers():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer;")
    data = cursor.fetchall()
    conn.close()
    return data
