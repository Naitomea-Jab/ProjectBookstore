# main.py
from bookstore.book_Manager import get_book, add_book, remove_book
from bookstore.customer_Manager import register_customer, get_customers, remove_customer, buy_book, \
    get_customer_purchases
from bookstore.monitor import *
from bookstore.utilities import initialize_database, validate_email
from bookstore.file_manager import export_data, import_data


def __main__():
    initialize_database()
    initialize_menu()


def statistics_menu():
    """Menu ze statystykami i raportami."""
    while True:
        print("\n=== MENU STATYSTYK ===")
        print("1. Całkowita liczba książek")
        print("2. Książki według autora")
        print("3. Książki niedostępne (brak w magazynie)")
        print("4. Całkowita liczba klientów")
        print("5. Całkowita liczba zakupów")
        print("6. Najpopularniejsze książki")
        print("7. Najnowsze książki")
        print("8. Książki według gatunków")
        print("9. Statystyki przychodów")
        print("10. Książki z niskim stanem magazynowym")
        print("11. Historia zakupów")
        print("12. Eksportuj dane do CSV")
        print("13. Importuj dane z CSV")
        print("14. Powrót do głównego menu")

        try:
            choice = int(input("Wpisz numer: "))

            match choice:
                case 1:
                    result = get_total_books()
                    print(f"Całkowita liczba książek: {result['data']}")

                case 2:
                    author = input("Podaj nazwę autora: ")
                    result = get_books_by_author(author)
                    if result['data']:
                        print(f"Książki autora {author}:")
                        for book in result['data']:
                            print(f"  - {book[1]} (ID: {book[0]}, Cena: {book[4]} zł, Stan: {book[5]})")
                    else:
                        print(f"Brak książek autora {author}")

                case 3:
                    result = get_ebooks_unavailable()
                    print(f"Liczba książek niedostępnych: {result['data']}")

                case 4:
                    result = get_total_customers()
                    print(f"Całkowita liczba klientów: {result['data']}")

                case 5:
                    result = get_total_purchases()
                    print(f"Liczba zakupów: {result['data']}")

                case 6:
                    amount = input("Ile najpopularniejszych książek wyświetlić? (domyślnie 3): ").strip()
                    amount = int(amount) if amount.isdigit() else 3
                    result = get_popular_books(amount)
                    if result['data']:
                        print("Najpopularniejsze książki:")
                        for book in result['data']:
                            print(f"  - {book[0]} by {book[1]} (Sprzedano: {book[2]} egz.)")  # Corrected indices
                    else:
                        print("Brak danych o sprzedaży")

                case 7:
                    days = input("Z ilu ostatnich dni? (domyślnie 30): ").strip()
                    days = int(days) if days.isdigit() else 30
                    result = get_recent_books(days)
                    if result['data']:
                        print(f"Książki dodane w ostatnich {days} dniach:")
                        for book in result['data']:
                            # Corrected index for DateAdded: book[3] instead of book[6]
                            print(f"  - {book[1]} by {book[2]} (Dodano: {book[3]})")
                    else:
                        print("Brak książek z tego okresu")

                case 8:
                    genre_input = input("Podaj gatunek: ").strip()
                    result = get_books_by_genre(genre_input)
                    if result['data']:
                        print("Książki według gatunków:")
                        for book in result['data']:
                            print(
                                f"  - {book[1]} by {book[2]} (Gatunek: {book[3]}, Cena: {book[4]} zł, Stan: {book[5]})")
                    else:
                        print("Brak danych o gatunkach")

                case 9:
                    result = get_revenue_statistics()
                    data = result['data']
                    print(f"Całkowity przychód: {data['total_revenue']:.2f} zł")
                    print(f"Przychód z ostatnich 30 dni: {data['monthly_revenue']:.2f} zł")

                case 10:
                    threshold = input("Próg niskiego stanu (domyślnie 5): ").strip()
                    threshold = int(threshold) if threshold.isdigit() else 5
                    result = get_low_stock_books(threshold)
                    if result['data']:
                        print(f"Książki z stanem ≤ {threshold}:")
                        for book in result['data']:
                            print(f"  - {book[1]} (Stan: {book[3]})")
                    else:
                        print("Wszystkie książki mają wystarczający stan magazynowy")

                case 11:
                    result = get_purchase_history()
                    if result['data']:
                        print("Ostatnie zakupy:")
                        for purchase in result['data'][:10]:  # Pokaż tylko 10 ostatnich
                            print(f"  - {purchase[1]} kupił {purchase[2]} (Ilość: {purchase[3]}, Data: {purchase[4]})")
                    else:
                        print("Brak historii zakupów")

                case 12:
                    print("\n--- Eksport danych do CSV ---")
                    table_choice = input(
                        "Wybierz tabelę do eksportu (Customers, Books, Purchases): ").strip().capitalize()
                    if table_choice in ['Customers', 'Books', 'Purchases']:
                        filename_input = input(
                            f"Podaj nazwę pliku CSV (domyślnie {table_choice.lower()}.csv): ").strip()
                        filename = filename_input if filename_input else None
                        result = export_data(table_choice, filename)
                        print(result["message"])
                    else:
                        print("Nieprawidłowa nazwa tabeli.")
                case 13:
                    print("\n--- Import danych z CSV ---")
                    table_choice = input(
                        "Wybierz tabelę do importu (Customers, Books, Purchases): ").strip().capitalize()
                    if table_choice in ['Customers', 'Books', 'Purchases']:
                        filename_input = input(
                            f"Podaj nazwę pliku CSV (domyślnie {table_choice.lower()}.csv): ").strip()
                        filename = filename_input if filename_input else None
                        result = import_data(table_choice, filename)
                        print(result["message"])
                    else:
                        print("Nieprawidłowa nazwa tabeli.")
                case 14:
                    break
                case _:
                    print("Nieprawidłowy wybór")
                    # conn.close() # Removed
        except ValueError:
            print("Proszę podać prawidłowy numer")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")


def add_book_to_system():
    print("\n--- Dodawanie nowej książki ---")
    title = input("Tytuł: ")
    author = input("Autor: ")
    genre = input("Gatunek: ")
    try:
        price = float(input("Cena: "))
        stock = int(input("Stan magazynowy: "))
    except ValueError:
        print("Cena i stan magazynowy muszą być liczbami.")
        return
    book_info = {
        'Title': title,
        'Author': author,
        'Genre': genre,
        'Price': price,
        'Stock': stock
    }
    result = add_book(book_info)
    print(result["message"])


def remove_book_from_system():
    print("\n--- Usuwanie książki ---")
    book_data = input("Podaj ID lub tytuł książki do usunięcia: ")
    result = remove_book(book_data)
    print(result["message"])


def show_all_books():
    print("\n--- Lista książek ---")
    result = get_book()
    if result["code"] == 200:
        for book in result["data"]:
            print(
                f"ID: {book[0]}, Tytuł: {book[1]}, Autor: {book[2]}, Gatunek: {book[3]}, Cena: {book[4]:.2f} zł, Stan: {book[5]}, Data dodania: {book[6]}")
    else:
        print(result["message"])


def register_new_customer():
    print("\n--- Rejestracja nowego klienta ---")
    name = input("Imię i nazwisko: ")
    email = input("Email: ")
    if validate_email(email):
        client_info = {
            'Name': name,
            'Email': email
        }
        result = register_customer(client_info)
        print(result["message"])
    else:
        print("Nieprawidłowy format adresu email.")


def remove_existing_customer():
    print("\n--- Usuwanie klienta ---")
    customer_data = input("Podaj ID lub imię i nazwisko klienta do usunięcia: ")
    result = remove_customer(customer_data)
    print(result["message"])


def show_all_customers():
    print("\n--- Lista klientów ---")
    result = get_customers()
    if result["code"] == 200:
        for customer in result["data"]:
            print(f"ID: {customer[0]}, Imię i nazwisko: {customer[1]}, Email: {customer[2]}")
    else:
        print(result["message"])


def purchase_book_process():
    print("\n--- Zakup książki ---")
    customer_name = input("Imię i nazwisko klienta lub ID: ")
    book_title = input("Tytuł książki lub ID: ")
    try:
        quantity = int(input("Ilość: "))
        if quantity <= 0:
            print("Ilość musi być liczbą dodatnią.")
            return

        result = buy_book(customer_name, book_title, quantity)
        print(result["message"])
    except ValueError:
        print("Nieprawidłowa ilość. Podaj liczbę całkowitą.")


def initialize_menu():
    """Główne menu aplikacji."""
    while True:
        print("\n=== SYSTEM ZARZĄDZANIA KSIĘGARNIĄ ===")
        print("1. Dodaj książkę")
        print("2. Usuń książkę")
        print("3. Wyświetl wszystkie książki")
        print("4. Zarejestruj klienta")
        print("5. Usuń klienta")
        print("6. Wyświetl wszystkich klientów")
        print("7. Kup książkę")
        print("8. Wyświetl historię zakupów klienta")
        print("9. Menu Statystyk")
        print("10. Wyjście")

        try:
            choice = int(input("Wpisz numer: "))

            match choice:
                case 1:
                    add_book_to_system()
                case 2:
                    remove_book_from_system()
                case 3:
                    show_all_books()
                case 4:
                    register_new_customer()
                case 5:
                    remove_existing_customer()
                case 6:
                    show_all_customers()
                case 7:
                    purchase_book_process()
                case 8:
                    print("\n--- Historia zakupów klienta ---")
                    customer_data = input("Wpisz ID lub pełne imię klienta: ")
                    result = get_customer_purchases(customer_data)
                    if result["code"] == 200:
                        print("\nHistoria zakupów:")
                        total_spent = 0
                        for purchase in result["data"]:
                            item_total = purchase[3] * purchase[5]  # quantity * price
                            total_spent += item_total
                            print(f"- {purchase[1]} kupił {purchase[2]}")
                            print(f"  Ilość: {purchase[3]}, Data: {purchase[4]}, Koszt: {item_total:.2f} zł")
                        print(f"\nŁączna kwota wydana: {total_spent:.2f} zł")
                    else:
                        print(result["message"])

                case 9:
                    statistics_menu()

                case 10:
                    print("Dziękujemy za korzystanie z systemu!")
                    break

                case _:
                    print("Nieprawidłowy wybór")

        except ValueError:
            print("Proszę podać prawidłowy numer")
        except Exception as e:
            print(f"Wystąpił błąd: {e}")


if __name__ == "__main__":
    __main__()
