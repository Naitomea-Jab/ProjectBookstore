# utilities.py
import os
import random
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILE_DIR = os.path.join(BASE_DIR, "DATABASE")
DB_PATH = os.path.join(BASE_DIR, "DATABASE", "bookstore.db")


def get_next_book_id(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM book")
    result = cursor.fetchone()[0]
    if result is None:
        return 1
    else:
        return result + 1


def get_new_customer_id(conn):
    cursor = conn.cursor()
    available = False
    while not available:
        id_test = random.randint(1000, 9999)
        cursor.execute("SELECT ID FROM customer")
        result = cursor.fetchall()
        result = [item[0] for item in result]
        if id_test not in result:
            available = True
    return id_test