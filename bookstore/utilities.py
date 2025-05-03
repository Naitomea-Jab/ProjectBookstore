# utilities.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "DATABASE", "bookstore.db")


def get_next_book_id(conn):
    """
    Pobiera następny dostępny identyfikator w tabeli `book`.

    Args:
        conn (sqlite3.Connection): Połączenie SQLite.

    Returns:
        int: Następny dostępny identyfikator w tabeli `book`.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM book")
    result = cursor.fetchone()[0]
    if result is None:
        return 101
    else:
        return result + 1


def get_next_customer_id(conn):
    """
    Pobiera następny dostępny identyfikator w tabeli `customer`.

    Args:
        conn (sqlite3.Connection): Połączenie SQLite.

    Returns:
        int: Następny dostępny identyfikator w tabeli `customer`.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) FROM customer")
    result = cursor.fetchone()[0]
    if result is None:
        return 201
    else:
        return result + 1