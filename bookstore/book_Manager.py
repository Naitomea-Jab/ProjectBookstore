# book_Manager.py
import sqlite3
from bookstore.utilities import DB_PATH, get_next_book_id
from datetime import datetime


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

                - ID (int): ID książki.

                - AUTHOR (str): Autor książki.

                - TITLE (str): Tytuł książki.

                - NO_EBOOK_AVAILABLE (int): Liczba dostępnych egzemplarzy.

                - CREATED (str): Data utworzenia książki.

                - UPDATED (str): Data ostatniej aktualizacji książki.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if data is None:
        cursor.execute("SELECT * FROM book;")
    elif data.isdigit():
        cursor.execute("SELECT * FROM book WHERE ID = ?;", (data,))
    else:
        cursor.execute("SELECT * FROM book WHERE TITLE = ?;", (data,))

    data = cursor.fetchall()
    if not data:
        conn.close()
        return {
            "code": 404,
            "message": "Nie znaleziono książki do wypisania."
        }
    conn.close()
    return {
        "code": 200,
        "message": "OK",
        "data": data
    }

def add_book(bookInfo):
    """
    Dodaje nową książkę do bazy danych.

    Args:
        bookInfo (list): Lista zawierająca informacje o książce w kolejności:

            - author (str): Imię i nazwisko autora.

            - title (str): Tytuł książki.

            - amount (int): Liczba dostępnych egzemplarzy (musi być >= 0).

    Returns:
        dict: Słownik zawierający:

            - code (int): Kod HTTP-stylu. 201 jeśli książka została dodana,
              400 jeśli podano niepoprawną ilość egzemplarzy.

            - message (str): Komunikat informujący o wyniku operacji.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    author = bookInfo[0]
    title = bookInfo[1]
    amount = bookInfo[2]
    if amount < 0:
        return {
            "code": 400,
            "message": "Nie poprawna ilość egzemplarzy."
        }
    id = get_next_book_id(conn)
    current_date = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        "INSERT INTO book (ID, AUTHOR, TITLE, NO_EBOOK_AVAILABLE, CREATED, UPDATED) VALUES (?, ?, ?, ?, ?, ?);",
        (id, author, title, amount, current_date, current_date)
    )

    conn.commit()
    conn.close()
    return {
        "code": 201,
        "message": "Dodano książkę",
    }

def remove_book(data):
    """
    Usuwa książkę z bazy danych na podstawie ID lub tytułu.

    Args:
        data (str): ID książki (liczba całkowita jako string) lub tytuł (string) do usunięcia.

    Returns:
        dict: Słownik zawierający:

            - code (int): Kod HTTP-stylu. 200 jeśli usunięto książkę, 404 jeśli nie znaleziono książki.

            - message (str): Komunikat opisujący wynik operacji.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if data.isdigit():
        cursor.execute("DELETE FROM book WHERE ID = ?;", (data,))
    else:
        cursor.execute("DELETE FROM book WHERE TITLE = ?;", (data,))

    deleted = cursor.rowcount
    conn.commit()
    conn.close()

    if deleted > 0:
        return {
            "code": 200,
            "message": f"Usunięto {deleted} książkę(ki) z bazy danych."
        }
    else:
        return {
            "code": 404,
            "message": "Nie znaleziono książki do usunięcia."
        }