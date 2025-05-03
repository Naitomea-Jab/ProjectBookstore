# main.py
from bookstore.customerManager import getCustomers
from bookstore.bookManager import getBook
from frontend.gui import startGui

def __main__():
    print("Launching GUI...")
    startGui()

    customers = getCustomers()
    print("Loaded customers:")
    for c in customers:
        print(c)

    books = getBook()
    print("Loaded books:")
    for b in books:
        print(b)


if __name__ == "__main__":
    __main__()
