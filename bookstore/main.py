# main.py
from turtledemo.paint import switchupdown

from bookstore.customer_Manager import get_customers
from bookstore.book_Manager import get_book, add_book, remove_book
from frontend.gui import startGui

def __main__():
    initialize_menu()

def initialize_menu():
    while True:
        print("1. Add book")
        print("2. remove book")
        print("3. get book")
        print("9. quit")
        choice = int(input("Wpisz numer: "))
        match choice:
            case 1:
                #do a questions and then pack answers into an array
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

            case 9:
                break
            case _:
                print("nie znaleziony")


if __name__ == "__main__":
    __main__()
