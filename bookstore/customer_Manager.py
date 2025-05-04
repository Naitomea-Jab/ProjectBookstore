# customer_Manager.py
from datetime import datetime
from dateutil.relativedelta import relativedelta
import sqlite3
from bookstore.utilities import DB_PATH, FILE_DIR,get_new_customer_id
import os

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

                - ID (int): ID klienta.

                - NAME (str): Imię i nazwisko klienta.

                - E-MAIL (str): Adres email klienta.

                - PHONE (str): Numer telefonu klienta.

                - CREATED (str): Data utworzenia klienta.

                - UPDATED (str): Data ostatniej aktualizacji klienta.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if data is None:
        cursor.execute("SELECT * FROM customer;")
    elif data.isdigit():
        cursor.execute("SELECT * FROM customer WHERE ID = ?;", (data,))
    else:
        cursor.execute("SELECT * FROM customer WHERE NAME = ?;", (data,))

    data = cursor.fetchall()
    if not data:
        conn.close()
        return {
            "code": 404,
            "message": "Nie znaleziono klienta do wypisania."
        }
    conn.close()
    return {
        "code": 200,
        "message": "OK",
        "data": data
    }

def get_addresses(data=None):
    """
    Pobiera adresy klientów z bazy danych. Można pobrać wszystkie adresy, adres dla
    określonego ID klienta lub adres dla klienta o określonym imieniu i nazwisku.

    Args:
        data (str, optional): ID klienta (jako string) lub imię i nazwisko klienta (jako string).
                              Jeśli brak argumentu (domyślnie None), pobierane są wszystkie adresy.

    Returns:
        dict: Słownik zawierający:

            - code (int): Kod HTTP. 200 jeśli adresy zostały znalezione, 404 jeśli brak wyników.

            - message (str): Komunikat o wyniku operacji (np. "Znaleziono adresy" lub "Brak adresów").

            - data (list, jeżeli kod = 200): Lista krotek zawierających dane o adresach. Zawiera pola:

                - ID (int): ID klienta, do którego należy adres.

                - STREET (str): Nazwa ulicy.

                - CITY (str): Nazwa miasta.

                - COUNTRY (str): Nazwa kraju.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if data is None:
        cursor.execute("SELECT * FROM address;")
    elif not data.isdigit():
        cursor.execute("SELECT ID FROM customer WHERE NAME = ?;", (data,))
        result = cursor.fetchone()
        if result:
            data = result[0]
        else:
            conn.close()
            return {
                "code": 404,
                "message": "Nie znaleziono adresu do wypisania."
            }
        cursor.execute("SELECT * FROM address WHERE ID = ?;", (data,))
    else:
        cursor.execute("SELECT * FROM address WHERE ID = ?;", (data,))
    data = cursor.fetchall()
    if not data:
        conn.close()
        return {
            "code": 404,
            "message": "Nie znaleziono adresu do wypisania."
        }
    conn.close()
    return {
        "code": 200,
        "message": "OK",
        "data": data
    }

def register_customer(clientInfo, addressInfo):
    """
      Rejestruje nowego klienta w bazie danych wraz z jego adresem.

      Args:
          clientInfo (list): Lista zawierająca informacje o kliencie w kolejności:

              - name (str): Imię i nazwisko klienta.

              - email (str): Adres email klienta.

              - phone (str): Numer telefonu klienta.
          addressInfo (list): Lista zawierająca informacje o adresie klienta w kolejności:

              - street (str): Nazwa ulicy.

              - city (str): Nazwa miasta.

              - country (str): Nazwa kraju.

      Returns:
          dict: Słownik zawierający:

              - code (int): Kod HTTP-stylu. 201 jeśli klient został zarejestrowany pomyślnie.

              - message (str, opcjonalny): Komunikat informujący o wyniku operacji.
      """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    client_id = get_new_customer_id(conn)
    current_date = datetime.now().strftime("%Y-%m-%d")

    name = clientInfo[0]
    email = clientInfo[1]
    phone = clientInfo[2]

    cursor.execute(
        "INSERT INTO customer (ID, NAME, 'E-MAIL', PHONE, CREATED, UPDATED) VALUES (?, ?, ?, ?, ?, ?);",
        (client_id, name, email, phone, current_date, current_date)
    )

    street = addressInfo[0]
    city = addressInfo[1]
    country = addressInfo[2]

    cursor.execute(
        "INSERT INTO address (ID, STREET, CITY, COUNTRY) VALUES (?, ?, ?, ?);",
        (client_id, street, city, country)
    )

    conn.commit()
    conn.close()
    filename = f"{client_id}.txt"
    file_path = os.path.join(FILE_DIR, filename)
    with open(file_path, "w") as file:
        file.write("")
    return {
        "code": 201,
        "message": "OK"
    }

def remove_customer(data):
    """
      Usuwa klienta i jego adres z bazy danych na podstawie ID lub imienia i nazwiska.

      Args:
          data (str): ID klienta (liczba całkowita jako string) lub imię i nazwisko klienta (string) do usunięcia.

      Returns:
          dict: Słownik zawierający:

              - code (int): Kod HTTP-stylu. 200 jeśli usunięto klienta, 404 jeśli nie znaleziono klienta.

              - message (str): Komunikat opisujący wynik operacji.
      """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if not data.isdigit():
        cursor.execute("SELECT ID FROM customer WHERE NAME = ?;", (data,))
        result = cursor.fetchone()
        if result:
            data = result[0]
        else:
            conn.close()
            return {
                "code": 404,
                "message": "Nie znaleziono klienta do usunięcia."
            }
    cursor.execute("DELETE FROM customer WHERE ID = ?;", (data,))
    cursor.execute("DELETE FROM address WHERE ID = ?;", (data,))

    deleted = cursor.rowcount
    conn.commit()
    conn.close()

    if deleted > 0:
        filename = f"{data}.txt"
        file_path = os.path.join(FILE_DIR, filename)
        os.remove(file_path)
        return {
            "code": 200,
            "message": f"Usunięto klienta z bazy danych."
        }
    else:
        return {
            "code": 404,
            "message": "Nie znaleziono klienta do usunięcia."
        }

def buy_book(client_id, book_data, duration):
    """
      Zakup książki przez klienta, zapisując informację o zakupie do pliku tekstowego klienta.

      Args:
          client_id (int): ID klienta dokonującego zakupu.
          book_data (list): Lista zawierająca dane o książce (powinna zawierać ID i tytuł na indeksach 0 i 2).
          duration (str): Czas trwania dostępu do książki w miesiącach (jako string).

      Returns:
          dict: Słownik zawierający:

              - code (int): Kod HTTP-stylu. 200 jeśli zakup został zarejestrowany pomyślnie.

              - message (str, opcjonalny): Komunikat informujący o wyniku operacji.
      """
    print(client_id)
    print(book_data)
    print(duration)

    date = datetime.now()
    expiry_date = date + relativedelta(months=int(duration))
    formated_date = date.strftime("%Y-%m-%d")
    formated_expiry_date = expiry_date.strftime("%Y-%m-%d")

    filename = f"{client_id}.txt"
    file_path = os.path.join(FILE_DIR, filename)
    with open(file_path, "a") as file:
        file.write(f"BookID: {book_data[0]}, Title: {book_data[2]}, PurchaseDate: {formated_date}, ExpiryDate: {formated_expiry_date};\n")
    return {
        "code": 200,
        "message": "OK"
    }