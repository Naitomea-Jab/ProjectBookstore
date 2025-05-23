# monitor.py
import sqlite3
from datetime import datetime, timedelta

from bookstore.utilities import DB_PATH  # Import DB_PATH


def get_total_books():
    """Zwraca całkowitą liczbę książek w bazie danych."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Books")
        return {
            "code": 200,
            "message": "OK",
            "data": cursor.fetchone()[0]
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania całkowitej liczby książek: {e}",
            "data": 0
        }
    finally:
        if conn:
            conn.close()


def get_books_by_author(author):
    """Zwraca wszystkie książki danego autora."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books WHERE Author = ?", (author,))
        books = cursor.fetchall()
        return {
            "code": 200 if books else 404,
            "message": "OK" if books else "Brak książek tego autora.",
            "data": books
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania książek według autora: {e}",
            "data": []
        }
    finally:
        if conn:
            conn.close()


def get_ebooks_unavailable():
    """Zwraca liczbę książek, które są niedostępne (stock = 0)."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Books WHERE Stock = 0")
        return {
            "code": 200,
            "message": "OK",
            "data": cursor.fetchone()[0]
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania niedostępnych książek: {e}",
            "data": 0
        }
    finally:
        if conn:
            conn.close()


def get_total_customers():
    """Zwraca całkowitą liczbę klientów."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Customers")
        return {
            "code": 200,
            "message": "OK",
            "data": cursor.fetchone()[0]
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania całkowitej liczby klientów: {e}",
            "data": 0
        }
    finally:
        if conn:
            conn.close()


def get_total_purchases():
    """Zwraca całkowitą liczbę zakupów."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM Purchases")
        return {
            "code": 200,
            "message": "OK",
            "data": cursor.fetchone()[0]
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania całkowitej liczby zakupów: {e}",
            "data": 0
        }
    finally:
        if conn:
            conn.close()


def get_popular_books(limit=5):
    """Zwraca najpopularniejsze książki na podstawie liczby zakupów."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
                       SELECT b.Title, b.Author, SUM(p.Quantity) as TotalQuantitySold
                       FROM Purchases p
                                JOIN Books b ON p.BookID = b.BookID
                       GROUP BY b.BookID
                       ORDER BY TotalQuantitySold DESC
                       LIMIT ?;
                       """, (limit,))
        books = cursor.fetchall()
        return {
            "code": 200 if books else 404,
            "message": "OK" if books else "Brak danych o popularnych książkach.",
            "data": books
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania popularnych książek: {e}",
            "data": []
        }
    finally:
        if conn:
            conn.close()


def get_recent_books(limit=5):
    """Zwraca ostatnio dodane książki."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT BookID, Title, Author, DateAdded FROM Books ORDER BY DateAdded DESC LIMIT ?;", (limit,))
        books = cursor.fetchall()
        return {
            "code": 200 if books else 404,
            "message": "OK" if books else "Brak danych o najnowszych książkach.",
            "data": books
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania najnowszych książek: {e}",
            "data": []
        }
    finally:
        if conn:
            conn.close()


def get_books_by_genre(genre):
    """Zwraca wszystkie książki danego gatunku."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Books WHERE Genre LIKE ?;", (f"%{genre}%",))
        books = cursor.fetchall()
        return {
            "code": 200 if books else 404,
            "message": "OK" if books else f"Brak książek w gatunku '{genre}'.",
            "data": books
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania książek według gatunku: {e}",
            "data": []
        }
    finally:
        if conn:
            conn.close()


def get_revenue_statistics():
    """Zwraca statystyki przychodów (całkowity przychód, przychód z ostatnich 30 dni)."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Całkowity przychód
        cursor.execute("""
                       SELECT SUM(p.Quantity * b.Price)
                       FROM Purchases p
                                JOIN Books b ON p.BookID = b.BookID;
                       """)
        total_revenue = cursor.fetchone()[0] or 0.0

        # Przychód z ostatnich 30 dni
        thirty_days_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
                       SELECT SUM(p.Quantity * b.Price)
                       FROM Purchases p
                                JOIN Books b ON p.BookID = b.BookID
                       WHERE p.PurchaseDate >= ?;
                       """, (thirty_days_ago,))
        monthly_revenue = cursor.fetchone()[0] or 0.0

        return {
            "code": 200,
            "message": "OK",
            "data": {
                "total_revenue": total_revenue,
                "monthly_revenue": monthly_revenue
            }
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania statystyk przychodów: {e}",
            "data": {"total_revenue": 0.0, "monthly_revenue": 0.0}
        }
    finally:
        if conn:
            conn.close()


def get_low_stock_books(threshold=10):
    """Zwraca książki z niskim stanem magazynowym (poniżej progu)."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT BookID, Title, Author, Stock FROM Books WHERE Stock > 0 AND Stock <= ? ORDER BY Stock ASC;",
            (threshold,))
        books = cursor.fetchall()
        return {
            "code": 200 if books else 404,
            "message": "OK" if books else "Brak książek z niskim stanem magazynowym.",
            "data": books
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania książek z niskim stanem magazynowym: {e}",
            "data": []
        }
    finally:
        if conn:
            conn.close()


def get_purchase_history(start_date=None, end_date=None):
    """Zwraca historię zakupów, opcjonalnie z filtrem daty."""
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if start_date and end_date:
            cursor.execute("""
                           SELECT p.PurchaseID,
                                  c.Name,
                                  b.Title,
                                  p.Quantity,
                                  p.PurchaseDate,
                                  (p.Quantity * b.Price) as TotalPrice
                           FROM Purchases p
                                    JOIN Customers c ON p.CustomerID = c.CustomerID
                                    JOIN Books b ON p.BookID = b.BookID
                           WHERE DATE(p.PurchaseDate) BETWEEN ? AND ?
                           ORDER BY p.PurchaseDate DESC
                           """, (start_date, end_date))
        else:
            cursor.execute("""
                           SELECT p.PurchaseID,
                                  c.Name,
                                  b.Title,
                                  p.Quantity,
                                  p.PurchaseDate,
                                  (p.Quantity * b.Price) as TotalPrice
                           FROM Purchases p
                                    JOIN Customers c ON p.CustomerID = c.CustomerID
                                    JOIN Books b ON p.BookID = b.BookID
                           ORDER BY p.PurchaseDate DESC
                           LIMIT 100
                           """)

        purchases = cursor.fetchall()
        return {
            "code": 200 if purchases else 404,
            "message": "OK" if purchases else "Brak historii zakupów.",
            "data": purchases
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania historii zakupów: {e}",
            "data": []
        }
    finally:
        if conn:
            conn.close()
