# bookManager.py
import sqlite3
from bookstore.utilities import DB_PATH

def getBook():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book;")
    data = cursor.fetchall()
    conn.close()
    return data