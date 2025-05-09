from tkinter import *
from tkinter.messagebox import showinfo, showerror


def start_gui():
    root = Tk()
    root.title("Sklep z książkami")
    root.geometry("800x500")

    # Logo/Baner
    Label(root, text="KSIĘGARNIA ONLINE", font=("Arial", 20), bg="lightblue").pack(fill=X, pady=10)

    # Główny kontener
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=1, padx=10, pady=5)

    # Lista książek (lewa strona)
    books_frame = Frame(main_frame)
    books_frame.pack(side=LEFT, fill=BOTH, expand=1)

    books = [
        {"title": "Wiedźmin: Ostatnie życzenie", "price": "39.99 zł", "author": "Andrzej Sapkowski"},
        {"title": "Harry Potter i Kamień Filozoficzny", "price": "34.99 zł", "author": "J.K. Rowling"},
        {"title": "Zbrodnia i Kara", "price": "29.99 zł", "author": "Fiodor Dostojewski"},
        {"title": "Lalka", "price": "27.99 zł", "author": "Bolesław Prus"}
    ]

    for i, book in enumerate(books):
        frame = Frame(books_frame, bd=1, relief=GROOVE, padx=10, pady=5)
        frame.pack(fill=X, pady=5)

        Label(frame, text=book["title"], font=("Arial", 10, "bold")).pack(anchor=W)
        Label(frame, text=book["author"]).pack(anchor=W)
        Label(frame, text=book["price"], fg="green").pack(anchor=W)
        Button(frame, text="Kup teraz", command=lambda b=book: showinfo("Kupiono", f"Kupiłeś: {b['title']}")).pack(
            anchor=E)

    # Panel logowania (prawa strona)
    login_frame = Frame(main_frame, bd=2, relief=GROOVE, width=250)
    login_frame.pack(side=RIGHT, fill=Y, padx=5)
    login_frame.pack_propagate(False)

    Label(login_frame, text="Panel użytkownika", font=("Arial", 12, "bold")).pack(pady=10)

    # Pola logowania
    Label(login_frame, text="Login:").pack()
    login_entry = Entry(login_frame)
    login_entry.pack()

    Label(login_frame, text="Hasło:").pack()
    password_entry = Entry(login_frame, show="*")
    password_entry.pack()

    # Przyciski logowania/rejestracji/wylogowania
    buttons_frame = Frame(login_frame)
    buttons_frame.pack(pady=5)

    login_btn = Button(buttons_frame, text="Zaloguj", width=10)
    login_btn.pack(side=LEFT, padx=2)

    register_btn = Button(buttons_frame, text="Rejestracja", width=10, command=lambda: Toplevel(root))
    register_btn.pack(side=LEFT, padx=2)

    logout_btn = Button(buttons_frame, text="Wyloguj", width=10, state=DISABLED)

    status = Label(login_frame, text="Status: Niezalogowany", fg="red")
    status.pack(pady=10)

    # Funkcje zarządzania stanem logowania
    def login():
        user = login_entry.get()
        pwd = password_entry.get()
        if user and pwd:
            status.config(text=f"Zalogowano: {user}", fg="green")
            login_btn.config(state=DISABLED)
            logout_btn.config(state=NORMAL)
            login_entry.config(state=DISABLED)
            password_entry.config(state=DISABLED)
            showinfo("Sukces", "Zalogowano pomyślnie!")
        else:
            showerror("Błąd", "Wprowadź login i hasło!")

    def logout():
        status.config(text="Status: Niezalogowany", fg="red")
        login_btn.config(state=NORMAL)
        logout_btn.config(state=DISABLED)
        login_entry.config(state=NORMAL)
        password_entry.config(state=NORMAL)
        login_entry.delete(0, END)
        password_entry.delete(0, END)
        showinfo("Wylogowano", "Zostałeś wylogowany")

    # Przypisanie komend do przycisków
    login_btn.config(command=login)
    logout_btn.config(command=logout)
    logout_btn.pack(side=LEFT, padx=2)  # Dodanie przycisku wyloguj do interfejsu

    root.mainloop()


if __name__ == "__main__":
    start_gui()