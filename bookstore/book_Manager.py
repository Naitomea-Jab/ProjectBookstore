# book_Manager.py
import sqlite3
from bookstore.utilities import DB_PATH
from datetime import datetime
import time


def log_performance(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Funkcja '{func.__name__}' wykonana w {end_time - start_time:.4f} sekund.")
        return result

    return wrapper


def get_book(data=None):
    """
    Pobiera książki z bazy danych. Można pobrać wszystkie książki, książki o
    określonym ID lub książki o określonym tytule.

    Args:
        data (str, optional): ID książki (jako string) lub tytuł książki (jako string).
                              Jeśli brak argumentu (domyślnie None), pobierane są wszystkie książki.

    Returns:
        dict: Słownik zawierający:

            - code (int): Kod HTTP. 200 jeśli książki zostały znalezione, 404 jeśli brak wyników.

            - message (str): Komunikat o wyniku operacji (np. "Znaleziono książki" lub "Brak książek").

            - data (list, jeżeli kod = 200): Lista krotek zawierających dane o książkach. Zawiera pola:
                - BookID (int): ID książki.
                - Title (str): Tytuł książki.
                - Author (str): Autor książki.
                - Genre (str): Gatunek książki.
                - Price (float): Cena książki.
                - Stock (int): Stan magazynowy książki.
                - DateAdded (str): Data dodania książki (ISO format YYYY-MM-DD HH:MM:SS).
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if data is None:
            cursor.execute("SELECT * FROM Books;")
        elif str(data).isdigit():  # Sprawdź, czy dane to cyfra (ID)
            cursor.execute("SELECT * FROM Books WHERE BookID = ?;", (data,))
        else:  # Zakładamy, że to tytuł
            cursor.execute("SELECT * FROM Books WHERE Title LIKE ?;", (f"%{data}%",))

        books = cursor.fetchall()

        if books:
            return {
                "code": 200,
                "message": "Znaleziono książki.",
                "data": books
            }
        else:
            return {
                "code": 404,
                "message": "Brak książek spełniających kryteria."
            }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania książek: {e}"
        }
    finally:
        if conn:
            conn.close()


@log_performance
def add_book(bookInfo):
    """
    Dodaje nową książkę do bazy danych.

    Args:
        bookInfo (dict): Słownik zawierający informacje o książce:
                         - Title (str): Tytuł książki.
                         - Author (str): Autor książki.
                         - Genre (str): Gatunek książki.
                         - Price (float): Cena książki.
                         - Stock (int): Stan magazynowy książki.

    Returns:
        dict: Słownik zawierający kod odpowiedzi i komunikat.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        title = bookInfo.get('Title')
        author = bookInfo.get('Author')
        genre = bookInfo.get('Genre')
        price = bookInfo.get('Price')
        stock = bookInfo.get('Stock')

        if not all([title, author, price is not None, stock is not None]):
            return {
                "code": 400,
                "message": "Brakuje wymaganych pól: Tytuł, Autor, Cena, Stan magazynowy."
            }

        if not isinstance(price, (int, float)) or price < 0:
            return {
                "code": 400,
                "message": "Cena musi być liczbą nieujemną."
            }
        if not isinstance(stock, int) or stock < 0:
            return {
                "code": 400,
                "message": "Stan magazynowy musi być liczbą całkowitą nieujemną."
            }

        date_added = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        cursor.execute("""
                       INSERT INTO Books (Title, Author, Genre, Price, Stock, DateAdded)
                       VALUES (?, ?, ?, ?, ?, ?);
                       """, (title, author, genre, price, stock, date_added))
        conn.commit()
        return {
            "code": 201,
            "message": f"Książka '{title}' została pomyślnie dodana."
        }
    except sqlite3.IntegrityError as e:
        return {
            "code": 409,  # Conflict
            "message": f"Błąd integralności danych: {e}. Możliwe, że książka o tym tytule i autorze już istnieje."
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas dodawania książki: {e}"
        }
    finally:
        if conn:
            conn.close()


def remove_book(data):
    """
    Usuwa książkę z bazy danych.

    Args:
        data (str): ID książki (jako string) lub tytuł książki (jako string).

    Returns:
        dict: Słownik zawierający kod odpowiedzi i komunikat.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if str(data).isdigit():  # Jeśli dane to cyfra (ID)
            cursor.execute("DELETE FROM Books WHERE BookID = ?;", (data,))
        else:  # Zakładamy, że to tytuł
            cursor.execute("DELETE FROM Books WHERE Title = ?;", (data,))

        deleted = cursor.rowcount
        conn.commit()
        return {
            "code": 200 if deleted > 0 else 404,
            "message": f"Usunięto {deleted} książkę(ki) z bazy danych." if deleted > 0 else "Nie znaleziono książki do usunięcia."
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas usuwania książki: {e}"
        }
    finally:
        if conn:
            conn.close()


def update_book_stock(book_id, quantity_change):
    """
    Aktualizuje stan magazynowy książki.

    Args:
        book_id (int): ID książki.
        quantity_change (int): Zmiana ilości (może być ujemna przy zakupie).

    Returns:
        dict: Słownik zawierający kod odpowiedzi i komunikat.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT Stock FROM Books WHERE BookID = ?;", (book_id,))
        result = cursor.fetchone()

        if not result:
            return {
                "code": 404,
                "message": "Nie znaleziono książki."
            }

        current_stock = result[0]
        new_stock = current_stock + quantity_change

        if new_stock < 0:
            return {
                "code": 400,
                "message": f"Nie można ustawić ujemnego stanu magazynowego. Obecny stan: {current_stock}, żądana zmiana: {quantity_change}"
            }

        cursor.execute("UPDATE Books SET Stock = ? WHERE BookID = ?;", (new_stock, book_id))
        conn.commit()

        if cursor.rowcount > 0:
            return {
                "code": 200,
                "message": f"Stan magazynowy książki o ID {book_id} zaktualizowany na {new_stock}."
            }
        else:
            return {
                "code": 404,
                "message": "Nie znaleziono książki do aktualizacji stanu magazynowego."
            }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas aktualizacji stanu magazynowego: {e}"
        }
    finally:
        if conn:
            conn.close()
