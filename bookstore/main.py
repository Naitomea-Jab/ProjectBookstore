# main.py
from bookstore.customerManager import getCustomers
from frontend.gui import startGui

def __main__():
    print("Launching GUI...")
    startGui()

    customers = getCustomers()
    print("Loaded customers:")
    for c in customers:
        print(c)

if __name__ == "__main__":
    __main__()
