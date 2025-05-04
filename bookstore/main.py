# main.py
from bookstore.book_Manager import get_book, add_book, remove_book
from bookstore.customer_Manager import register_customer, get_customers, get_addresses, remove_customer, buy_book
from frontend.gui import start_gui
from bookstore.monitor import *
import sqlite3
from bookstore.utilities import DB_PATH

def __main__():
    start_gui()
    initialize_menu()
def statistics_menu():
    while True:
        print("1. get total books")
        print("2. get books by author")
        print("3. get books that are unavailable")
        print("4. get total customers")
        print("5. get total purchases")
        print("6. get most popular books")
        print("7. get newest books")
        print("8. get customers number by countries")
        print("9. return to normal menu")
        conn = sqlite3.connect(DB_PATH)
        choice = int(input("Wpisz numer: "))
        match choice:
            case 1:
                result = get_total_books(conn)
                print(result["data"])
            case 2:
                result = get_books_by_author(conn, "Jarek Bondi")
                print(result["data"])
            case 3:
                result = get_ebooks_unavailable(conn)
                print(result["data"])
            case 4:
                result = get_total_customers(conn)
                print(result["data"])
            case 5:
                result = get_total_purchases(conn, 204)
                print(result["data"])
            case 6:
                result = get_most_popular_books(conn)
                print(result["data"])
            case 7:
                result = get_newest_books(conn)
                print(result["data"])
            case 8:
                result = get_customer_countries(conn)
                print(result["data"])
            case 9:
                conn.close()
                break;
            case _:
                print("invalid value")

def initialize_menu():
    while True:
        print("1. Add book")
        print("2. remove book")
        print("3. get book")
        print("4. register new customer")
        print("5. remove customer")
        print("6. buy book")
        print("7. all customers")
        print("8. all addresses")
        print("9. statistics menu")
        print("10. quit")
        choice = int(input("Wpisz numer: "))
        match choice:
            case 1:
                author = input("Wpisz author: ")
                title = input("Wpisz title: ")
                amount = int(input("Wpisz amount: "))
                bookInfo = [author, title, amount]
                add_book(bookInfo)

            case 2:
                infoToDelete = input("Wprowadz ID lub tytuł książki do usunięcia: ")
                result = remove_book(infoToDelete)
                if result["code"] == 404:
                    print(result["message"])

            case 3:
                info = input("Wprowadz ID lub tytuł książki do wypisania, brak wypisze wszystkie: ")
                if not info.strip():
                    info = None
                result = get_book(info)
                if result["code"] == 200:
                    for b in result["data"]:
                        print(b)
                else:
                    print(result["message"])

            case 4:
                print("Personalne informacje")
                name = input("Wpisz imie i nazwisko: ")
                email = input("Wpisz email: ")
                phone = input("Wpisz numer telefonu: ")
                print("Adres")
                street = input("Wpisz ulicę: ")
                city = input("Wpisz miasto: ")
                country = input("Wpisz kraj: ")
                clientInfo = [name, email, phone]
                addressInfo = [street, city, country]
                register_customer(clientInfo, addressInfo)

            case 5:
                infoToDelete = input("Wprowadz ID lub pełne imie klienta do usunięcia: ")
                result = remove_customer(infoToDelete)
                if result["code"] == 404:
                    print(result["message"])

            case 6:
                customer_id = input("Wpisz ID lub pełne imie klienta: ")
                result = get_customers(customer_id)
                if result["code"] == 404:
                    print(result["message"])
                    continue
                customer_id = result["data"][0][0]
                book_id = input("Wpisz ID lub tytuł książki do zakupu: ")
                book_data = get_book(book_id)
                if book_data["code"] == 404:
                    print(book_data["message"])
                    continue
                months_to_buy = input("Wpisz na ile miesięcy chcesz kupić książkę: ")
                buy_book(customer_id, book_data["data"][0], months_to_buy)


            case 7:
                info = input("Wprowadz ID lub pełne imie klienta do wypisania, brak wypisze wszystkie: ")
                if not info.strip():
                    info = None
                result = get_customers(info)
                if result["code"] == 200:
                    for b in result["data"]:
                        print(b)
                else:
                    print(result["message"])
            case 8:
                info = input("Wprowadz ID lub pełne imie do wypisania adresu, brak wypisze wszystkie: ")
                if not info.strip():
                    info = None
                result = get_addresses(info)
                if result["code"] == 200:
                    for b in result["data"]:
                        print(b)
                else:
                    print(result["message"])

            case 9:
                statistics_menu()

            case 10:
                break
            case _:
                print("nie znaleziony")


if __name__ == "__main__":
    __main__()
