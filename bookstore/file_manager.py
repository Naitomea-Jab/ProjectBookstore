# bookstore/file_manager.py
import sqlite3
import pandas as pd
import os
from bookstore.utilities import DB_PATH, FILE_DIR

CSV_DIR = FILE_DIR

os.makedirs(CSV_DIR, exist_ok=True)


def export_data(table_name, filename=None):
    """
    Eksportuje dane z podanej tabeli do pliku CSV w folderze DATABASE.

    Args:
        table_name (str): Nazwa tabeli do eksportu ('Customers', 'Books', 'Purchases').
        filename (str, optional): Nazwa pliku CSV. Domyślnie 'nazwa_tabeli.csv'.

    Returns:
        dict: Słownik z kodem odpowiedzi i komunikatem.
    """
    if filename is None:
        csv_filename = f"{table_name.lower()}.csv"
    else:
        csv_filename = filename

    full_path = os.path.join(CSV_DIR, csv_filename)

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(f"SELECT * FROM {table_name};", conn)
        df.to_csv(full_path, index=False)
        return {
            "code": 200,
            "message": f"Dane z tabeli '{table_name}' zostały pomyślnie wyeksportowane do '{full_path}'."
        }
    except sqlite3.Error as e:
        return {
            "code": 404,
            "message": f"Błąd bazy danych podczas eksportu tabeli '{table_name}': {e}"
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"Wystąpił nieoczekiwany błąd podczas eksportu danych: {e}"
        }
    finally:
        if conn:
            conn.close()


def import_data(table_name, filename=None):
    """
    Importuje dane z pliku CSV z folderu DATABASE do podanej tabeli.

    Args:
        table_name (str): Nazwa tabeli do importu ('Customers', 'Books', 'Purchases').
        filename (str, optional): Nazwa pliku CSV. Domyślnie 'nazwa_tabeli.csv'.

    Returns:
        dict: Słownik z kodem odpowiedzi i komunikatem.
    """
    if filename is None:
        csv_filename = f"{table_name.lower()}.csv"
    else:
        csv_filename = filename

    full_path = os.path.join(CSV_DIR, csv_filename)

    if not os.path.exists(full_path):
        return {
            "code": 404,
            "message": f"Plik '{full_path}' nie został znaleziony."
        }

    conn = None
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_csv(full_path)

        if table_name == 'Customers':
            for index, row in df.iterrows():
                try:
                    conn.execute("""
                                 INSERT INTO Customers (CustomerID, Name, Email)
                                 VALUES (?, ?, ?)
                                 ON CONFLICT(CustomerID) DO UPDATE SET Name=excluded.Name,
                                                                       Email=excluded.Email;
                                 """, (row['CustomerID'], row['Name'], row['Email']))
                except sqlite3.IntegrityError as e:
                    if "UNIQUE constraint failed: Customers.Email" in str(e):
                        print(
                            f"Ostrzeżenie: Klient z adresem email '{row['Email']}' już istnieje. Pomijanie wiersza {index + 2}.")
                    else:
                        print(
                            f"Błąd integralności danych podczas importu Customers w wierszu {index + 2}: {e}. Pomijanie wiersza.")
                        continue
            conn.commit()
            return {
                "code": 200,
                "message": f"Dane do tabeli '{table_name}' zostały pomyślnie zaimportowane z '{full_path}'."
            }

        elif table_name == 'Books':
            for index, row in df.iterrows():
                cursor = conn.execute("SELECT BookID FROM Books WHERE Title = ? AND Author = ?;",
                                      (row['Title'], row['Author']))
                existing_book = cursor.fetchone()
                if existing_book:
                    conn.execute("""
                                 UPDATE Books
                                 SET Genre=?,
                                     Price=?,
                                     Stock=?,
                                     DateAdded=?
                                 WHERE BookID = ?;
                                 """, (row['Genre'], row['Price'], row['Stock'], row['DateAdded'], existing_book[0]))
                else:
                    conn.execute("""
                                 INSERT INTO Books (Title, Author, Genre, Price, Stock, DateAdded)
                                 VALUES (?, ?, ?, ?, ?, ?);
                                 """, (row['Title'], row['Author'], row['Genre'], row['Price'], row['Stock'],
                                       row['DateAdded']))
            conn.commit()
            return {
                "code": 200,
                "message": f"Dane do tabeli '{table_name}' zostały pomyślnie zaimportowane z '{full_path}'."
            }

        elif table_name == 'Purchases':
            expected_columns = ['CustomerID', 'BookID', 'Quantity', 'PurchaseDate']
            if not all(col in df.columns for col in expected_columns):
                return {
                    "code": 400,
                    "message": f"Plik CSV dla 'Purchases' ({full_path}) musi zawierać kolumny: CustomerID, BookID, Quantity, PurchaseDate."
                }

            for index, row in df.iterrows():
                customer_exists = conn.execute("SELECT 1 FROM Customers WHERE CustomerID = ?;",
                                               (row['CustomerID'],)).fetchone()
                book_exists = conn.execute("SELECT 1 FROM Books WHERE BookID = ?;", (row['BookID'],)).fetchone()

                if not customer_exists:
                    print(
                        f"Ostrzeżenie: CustomerID '{row['CustomerID']}' nie istnieje w bazie danych. Pomijanie zakupu w wierszu {index + 2} z pliku '{filename}'.")
                    continue
                if not book_exists:
                    print(
                        f"Ostrzeżenie: BookID '{row['BookID']}' nie istnieje w bazie danych. Pomijanie zakupu w wierszu {index + 2} z pliku '{filename}'.")
                    continue

                try:
                    purchase_date = pd.to_datetime(row['PurchaseDate']).strftime('%Y-%m-%d %H:%M:%S')
                except ValueError:
                    print(
                        f"Ostrzeżenie: Nieprawidłowy format daty '{row['PurchaseDate']}' w wierszu {index + 2} z pliku '{filename}'. Użyto bieżącej daty.")
                    purchase_date = pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')

                try:
                    conn.execute("""
                                 INSERT INTO Purchases (CustomerID, BookID, Quantity, PurchaseDate)
                                 VALUES (?, ?, ?, ?);
                                 """, (row['CustomerID'], row['BookID'], row['Quantity'], purchase_date))
                except sqlite3.IntegrityError as e:
                    print(
                        f"Błąd integralności danych podczas importu Purchases w wierszu {index + 2} z pliku '{filename}': {e}. Pomijanie wiersza.")
                    continue

            conn.commit()
            return {
                "code": 200,
                "message": f"Dane do tabeli '{table_name}' zostały pomyślnie zaimportowane z '{full_path}'."
            }
        else:
            return {
                "code": 400,
                "message": f"Nieznana nazwa tabeli: '{table_name}'."
            }

    except pd.errors.EmptyDataError:
        return {
            "code": 400,
            "message": f"Plik '{full_path}' jest pusty lub nie zawiera danych."
        }
    except pd.errors.ParserError as e:
        return {
            "code": 400,
            "message": f"Błąd parsowania pliku CSV '{full_path}': {e}"
        }
    except Exception as e:
        return {
            "code": 500,
            "message": f"Wystąpił nieoczekiwany błąd podczas importu danych: {e}"
        }
    finally:
        if conn:
            conn.close()
