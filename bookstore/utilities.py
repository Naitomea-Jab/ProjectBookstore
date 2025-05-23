# utilities.py
import os
import uuid
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILE_DIR = os.path.join(BASE_DIR, "DATABASE")
DB_PATH = os.path.join(BASE_DIR, "DATABASE", "bookstore_main.db")


def get_next_book_id(conn):
    """
    Pobiera następny dostępny ID książki.
    Uwaga: Ta funkcja nie jest już potrzebna, ponieważ BookID jest AUTO_INCREMENT.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(BookID) FROM Books")
    result = cursor.fetchone()[0]
    if result is None:
        return 1
    else:
        return result + 1


def generate_customer_id():
    """
    Generuje unikalny UUID dla nowego klienta.

    Returns:
        str: Unikalny identyfikator UUID w formacie string.
    """
    return str(uuid.uuid4())


def validate_email(email):
    """
    Podstawowa walidacja adresu email.

    Args:
        email (str): Adres email do walidacji.

    Returns:
        bool: True jeśli email jest poprawny, False w przeciwnym razie.
    """
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def initialize_database():
    """
    Inicjalizuje bazę danych: tworzy plik bazy danych i tabele, jeśli nie istnieją.
    """
    os.makedirs(FILE_DIR, exist_ok=True)

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Tworzenie tabeli Customers
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS Customers
                       (
                           CustomerID TEXT PRIMARY KEY,
                           Name       TEXT        NOT NULL,
                           Email      TEXT UNIQUE NOT NULL
                       )
                       """)

        # Tworzenie tabeli Books
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS Books
                       (
                           BookID    INTEGER PRIMARY KEY AUTOINCREMENT,
                           Title     TEXT NOT NULL,
                           Author    TEXT NOT NULL,
                           Genre     TEXT,
                           Price     REAL NOT NULL,
                           Stock     INTEGER DEFAULT 0,
                           DateAdded TEXT
                       )
                       """)

        # Tworzenie tabeli Purchases
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS Purchases
                       (
                           PurchaseID   INTEGER PRIMARY KEY AUTOINCREMENT,
                           CustomerID   TEXT    NOT NULL,
                           BookID       INTEGER NOT NULL,
                           Quantity     INTEGER  DEFAULT 1,
                           PurchaseDate DATETIME DEFAULT CURRENT_TIMESTAMP,
                           FOREIGN KEY (CustomerID) REFERENCES Customers (CustomerID),
                           FOREIGN KEY (BookID) REFERENCES Books (BookID)
                       )
                       """)

        conn.commit()
    except sqlite3.Error as e:
        print(f"Błąd bazy danych podczas inicjalizacji: {e}")
    finally:
        if conn:
            conn.close()
