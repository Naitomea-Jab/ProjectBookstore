# customer_Manager.py
import sqlite3
from bookstore.utilities import DB_PATH, generate_customer_id
from datetime import datetime


def get_customers(data=None):
    """
    Pobiera klientów z bazy danych. Można pobrać wszystkich klientów, klientów o
    określonym ID lub klientów o określonym imieniu i nazwisku.

    Args:
        data (str, optional): ID klienta (jako string) lub imię i nazwisko klienta (jako string).
                              Jeśli brak argumentu (domyślnie None), pobierani są wszyscy klienci.

    Returns:
        dict: Słownik zawierający:

            - code (int): Kod HTTP. 200 jeśli klienci zostali znalezieni, 404 jeśli brak wyników.

            - message (str): Komunikat o wyniku operacji (np. "Znaleziono klientów" lub "Brak klientów").

            - data (list, jeżeli kod = 200): Lista krotek zawierających dane o klientach. Zawiera pola:

                - CustomerID (str): ID klienta.

                - Name (str): Imię i nazwisko klienta.

                - Email (str): Adres email klienta.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if data is None:
            cursor.execute("SELECT * FROM Customers;")
        elif len(data) == 36 and '-' in data:  # Assume UUID format for ID
            cursor.execute("SELECT * FROM Customers WHERE CustomerID = ?;", (data,))
        else:  # Assume it's a name
            cursor.execute("SELECT * FROM Customers WHERE Name LIKE ?;", (f"%{data}%",))

        customers = cursor.fetchall()

        if customers:
            return {
                "code": 200,
                "message": "Znaleziono klientów.",
                "data": customers
            }
        else:
            return {
                "code": 404,
                "message": "Brak klientów spełniających kryteria."
            }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania klientów: {e}"
        }
    finally:
        if conn:
            conn.close()


def register_customer(clientInfo):
    """
    Rejestruje nowego klienta w bazie danych.

    Args:
        clientInfo (dict): Słownik zawierający informacje o kliencie:
                           - Name (str): Imię i nazwisko klienta.
                           - Email (str): Adres email klienta.

    Returns:
        dict: Słownik zawierający kod odpowiedzi i komunikat.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        name = clientInfo.get('Name')
        email = clientInfo.get('Email')

        if not all([name, email]):
            return {
                "code": 400,
                "message": "Brakuje wymaganych pól: Imię i nazwisko, Email."
            }
        cursor.execute("SELECT CustomerID FROM Customers WHERE Email = ?;", (email,))
        if cursor.fetchone():
            return {
                "code": 409,  # Conflict
                "message": "Klient z podanym adresem email już istnieje."
            }

        customer_id = generate_customer_id()
        cursor.execute("""
                       INSERT INTO Customers (CustomerID, Name, Email)
                       VALUES (?, ?, ?);
                       """, (customer_id, name, email))
        conn.commit()
        return {
            "code": 201,
            "message": f"Klient '{name}' został pomyślnie zarejestrowany. ID: {customer_id}"
        }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas rejestracji klienta: {e}"
        }
    finally:
        if conn:
            conn.close()


def remove_customer(data):
    """
    Usuwa klienta z bazy danych wraz z jego zakupami.

    Args:
        data (str): ID klienta (jako string) lub imię i nazwisko klienta (jako string).

    Returns:
        dict: Słownik zawierający kod odpowiedzi i komunikat.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        customer_id = None
        if len(data) == 36 and '-' in data:  # UUID format
            customer_id = data
        else:
            cursor.execute("SELECT CustomerID FROM Customers WHERE Name = ?;", (data,))
            result = cursor.fetchone()
            if result:
                customer_id = result[0]

        if not customer_id:
            return {
                "code": 404,
                "message": "Nie znaleziono klienta do usunięcia."
            }

        conn.execute("BEGIN TRANSACTION;")
        cursor.execute("DELETE FROM Purchases WHERE CustomerID = ?;", (customer_id,))
        purchases_deleted = cursor.rowcount
        cursor.execute("DELETE FROM Customers WHERE CustomerID = ?;", (customer_id,))
        customer_deleted = cursor.rowcount
        conn.commit()
        return {
            "code": 200,
            "message": f"Usunięto {customer_deleted} klienta i {purchases_deleted} zakupów z bazy danych."
        }
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas usuwania klienta: {e}"
        }
    finally:
        if conn:
            conn.close()


def buy_book(customer_data, book_data, quantity):
    """
    Obsługuje proces zakupu książki.

    Args:
        customer_data (str): ID klienta lub imię i nazwisko.
        book_data (str): ID książki lub tytuł książki.
        quantity (int): Liczba kupowanych książek.

    Returns:
        dict: Słownik zawierający kod odpowiedzi i komunikat.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        customer_id = None
        if len(customer_data) == 36 and '-' in customer_data:  # UUID format
            cursor.execute("SELECT CustomerID FROM Customers WHERE CustomerID = ?;", (customer_data,))
            result = cursor.fetchone()
            if result:
                customer_id = result[0]
        else:
            cursor.execute("SELECT CustomerID FROM Customers WHERE Name = ?;", (customer_data,))
            result = cursor.fetchone()
            if result:
                customer_id = result[0]

        if not customer_id:
            return {
                "code": 404,
                "message": "Nie znaleziono klienta."
            }

        book_id = None
        stock = 0
        if str(book_data).isdigit():
            cursor.execute("SELECT BookID, Stock, Price FROM Books WHERE BookID = ?;", (book_data,))
            result = cursor.fetchone()
            if result:
                book_id, stock, price = result
        else:
            cursor.execute("SELECT BookID, Stock, Price FROM Books WHERE Title = ?;", (book_data,))
            result = cursor.fetchone()
            if result:
                book_id, stock, price = result

        if not book_id:
            return {
                "code": 404,
                "message": "Nie znaleziono książki."
            }

        if stock < quantity:
            return {
                "code": 400,
                "message": f"Brak wystarczającej ilości książek w magazynie. Dostępne: {stock}"
            }

        purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
                       INSERT INTO Purchases (CustomerID, BookID, Quantity, PurchaseDate)
                       VALUES (?, ?, ?, ?);
                       """, (customer_id, book_id, quantity, purchase_date))

        cursor.execute("UPDATE Books SET Stock = Stock - ? WHERE BookID = ?;", (quantity, book_id))

        conn.commit()
        return {
            "code": 200,
            "message": f"Zakup zrealizowany pomyślnie! Książka o ID {book_id} (Ilość: {quantity}) dla klienta o ID {customer_id}."
        }
    except sqlite3.Error as e:
        if conn:
            conn.rollback()
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas zakupu książki: {e}"
        }
    finally:
        if conn:
            conn.close()


def get_customer_purchases(customer_data):
    """
    Pobiera historię zakupów dla konkretnego klienta.

    Args:
        customer_data (str): ID klienta (jako string) lub imię i nazwisko klienta (jako string).

    Returns:
        dict: Słownik zawierający kod odpowiedzi i komunikat.
            - code (int): Kod HTTP (200, 404, 500).
            - message (str): Komunikat o wyniku operacji.
            - data (list, jeżeli kod = 200): Lista krotek z danymi o zakupach.
    """
    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        customer_id = None
        if len(customer_data) == 36 and '-' in customer_data:  # UUID format
            cursor.execute("SELECT CustomerID FROM Customers WHERE CustomerID = ?;", (customer_data,))
            result = cursor.fetchone()
            if result:
                customer_id = result[0]
        else:
            cursor.execute("SELECT CustomerID FROM Customers WHERE Name = ?;", (customer_data,))
            result = cursor.fetchone()
            if result:
                customer_id = result[0]

        if not customer_id:
            return {
                "code": 404,
                "message": "Nie znaleziono klienta."
            }

        cursor.execute("""
                       SELECT p.PurchaseID, c.Name, b.Title, p.Quantity, p.PurchaseDate, b.Price
                       FROM Purchases p
                                JOIN Books b ON p.BookID = b.BookID
                                JOIN Customers c ON p.CustomerID = c.CustomerID
                       WHERE p.CustomerID = ?
                       ORDER BY p.PurchaseDate DESC;
                       """, (customer_id,))

        purchases = cursor.fetchall()

        if purchases:
            return {
                "code": 200,
                "message": "Znaleziono historię zakupów.",
                "data": purchases
            }
        else:
            return {
                "code": 404,
                "message": "Brak historii zakupów dla tego klienta."
            }
    except sqlite3.Error as e:
        return {
            "code": 500,
            "message": f"Błąd bazy danych podczas pobierania historii zakupów klienta: {str(e)}"
        }
    finally:
        if conn:
            conn.close()
