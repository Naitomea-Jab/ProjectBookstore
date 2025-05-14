from tkinter import *
from tkinter.messagebox import showinfo
from bookstore.book_Manager import get_book

BOOK_WIDTH = 200
MARGIN = 20

def create_books(books_frame, books, columns):
    for widget in books_frame.winfo_children():
        widget.destroy()

    rows = (len(books) + columns - 1) // columns
    for r in range(rows):
        row_frame = Frame(books_frame)
        row_frame.pack(fill=X, pady=5)

        for c in range(columns):
            index = r * columns + c
            if index >= len(books):
                break

            book = books[index]
            frame = Frame(row_frame, bd=1, relief=GROOVE, width=BOOK_WIDTH, height=100, padx=10, pady=5)
            frame.pack(side=LEFT, padx=5, expand=1)
            frame.pack_propagate(False)

            Label(frame, text=book[2], font=("Arial", 10, "bold")).pack(anchor=W)
            Label(frame, text=f"Autor: {book[1]}").pack(anchor=W)
            Button(frame, text="Kup teraz",
                   command=lambda t=book[2]: showinfo("Kupiono", f"Kupiłeś: {t}")).pack(anchor=E)

def start_gui():
    root = Tk()
    root.title("Sklep z książkami")
    root.geometry("1000x600")

    Label(root, text="KSIĘGARNIA ONLINE", font=("Arial", 20), bg="#add8e6").pack(fill=X, pady=10)

    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=1)

    books_frame = Frame(main_frame)
    books_frame.pack(side=LEFT, fill=BOTH, expand=1, padx=10)

    login_frame = Frame(main_frame, bd=2, relief=GROOVE, padx=10, pady=10, bg="#f0f0f0")
    login_frame.pack(side=RIGHT, fill=Y, padx=10, pady=10)

    Label(login_frame, text="Logowanie", font=("Arial", 12, "bold"), bg="#f0f0f0").grid(row=0, columnspan=2, pady=5)
    Label(login_frame, text="Login:", bg="#f0f0f0").grid(row=1, column=0, sticky=W, pady=2)
    Entry(login_frame).grid(row=1, column=1, pady=2)
    Label(login_frame, text="Hasło:", bg="#f0f0f0").grid(row=2, column=0, sticky=W, pady=2)
    Entry(login_frame, show="*").grid(row=2, column=1, pady=2)
    Button(login_frame, text="Zaloguj", command=lambda: showinfo("Info", "Funkcja logowania")).grid(row=3, columnspan=2, pady=10)

    result = get_book()
    if result["code"] != 200:
        Label(books_frame, text=result["message"], fg="red").pack()
        root.mainloop()
        return

    books = result["data"]
    last_columns = [0]  # Użycie listy jako mutowalnej zmiennej

    def safe_resize(event):
        try:
            width = books_frame.winfo_width()
            if width < 1:
                return
            columns = max(1, width // (BOOK_WIDTH + MARGIN))
            if columns != last_columns[0]:  # aktualizuj tylko gdy ilość kolumn się zmienia
                last_columns[0] = columns
                create_books(books_frame, books, columns)
        except Exception as e:
            print("Resize error:", e)

    root.bind("<Configure>", safe_resize)
    root.after(100, lambda: safe_resize(None))

    root.mainloop()

if __name__ == "__main__":
    start_gui()
