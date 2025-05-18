# Import niezbędnych modułów
from tkinter import *  # Import głównego modułu Tkinter do tworzenia GUI
from tkinter.messagebox import showinfo  # Import funkcji do wyświetlania okien dialogowych
from bookstore.book_Manager import remove_book, add_book  # Import funkcji do zarządzania książkami
from bookstore.customer_Manager import remove_customer  # Import funkcji do zarządzania użytkownikami


def start_admin_panel():
    """
    Główna funkcja tworząca i uruchamiająca panel administratora.
    Panel jest otwierany jako nowe okno (Toplevel) i zawiera dwie główne sekcje:
    - Zarządzanie użytkownikami (lewa kolumna)
    - Zarządzanie książkami (prawa kolumna)
    """

    # Inicjalizacja okna panelu administratora
    admin_root = Toplevel()  # Tworzy nowe okno podrzędne (nie główne)
    admin_root.title("Panel administratora")  # Ustawia tytuł okna
    admin_root.geometry("1000x600")  # Ustawia początkowy rozmiar okna (szerokość x wysokość w pikselach)

    # Główny kontener dla całej zawartości panelu
    # Frame to prostokątny obszar służący do grupowania i rozmieszczania innych widgetów
    main_container = Frame(admin_root)
    # pack() umieszcza kontener w oknie z opcjami:
    # - fill=BOTH - rozciąga się w obu kierunkach (X i Y)
    # - expand=True - pozwala na rozszerzanie przy zmianie rozmiaru okna
    # - padx/pady=10 - marginesy wewnętrzne (w pikselach)
    main_container.pack(fill=BOTH, expand=True, padx=10, pady=10)

    # ======================================================================
    # LEWA KOLUMNA - ZARZĄDZANIE UŻYTKOWNIKAMI
    # ======================================================================

    # LabelFrame - ramka z etykietą, służy do logicznego grupowania elementów
    user_frame = LabelFrame(main_container, text="Zarządzanie użytkownikami", padx=15, pady=15)
    # Rozmieszczenie ramki:
    # - side=LEFT - przykleja do lewej strony kontenera
    # - fill=BOTH - wypełnia dostępną przestrzeń
    # - expand=True - pozwala na rozszerzanie
    user_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)

    # Etykieta sekcji usuwania użytkowników
    # font=("Arial", 10, "bold") - czcionka Arial, rozmiar 10, pogrubiona
    Label(user_frame, text="Usuń użytkownika:", font=("Arial", 10, "bold")).pack(anchor=W, pady=5)

    # Dodatkowa ramka dla lepszego rozmieszczenia elementów formularza
    user_control_frame = Frame(user_frame)
    user_control_frame.pack(fill=X, pady=5)  # fill=X - rozciąga się tylko w poziomie

    # Etykieta pola wprowadzania danych
    Label(user_control_frame, text="ID/Nazwa:").pack(side=LEFT, padx=5)

    # Pole wprowadzania danych (Entry)
    user_delete_entry = Entry(user_control_frame, width=25)
    # Rozmieszczenie pola:
    # - side=LEFT - umieszcza po lewej stronie
    # - expand=True - pozwala na rozszerzanie
    # - fill=X - wypełnia dostępną przestrzeń w poziomie
    user_delete_entry.pack(side=LEFT, padx=5, expand=True, fill=X)

    # Przycisk "Usuń" z obsługą zdarzenia
    Button(user_control_frame, text="Usuń",
           # Lambda wyrażenie tworzy anonimową funkcję, która:
           # 1. Pobiera aktualną wartość z user_delete_entry (get())
           # 2. Przekazuje ją do funkcji remove_user_action
           # Dzięki lambda, funkcja zostanie wywołana dopiero po kliknięciu,
           # a nie podczas tworzenia przycisku
           command=lambda: remove_user_action(user_delete_entry.get())) \
        .pack(side=LEFT, padx=5)

    # ======================================================================
    # PRAWA KOLUMNA - ZARZĄDZANIE KSIĄŻKAMI
    # ======================================================================

    book_frame = LabelFrame(main_container, text="Zarządzanie książkami", padx=15, pady=15)
    book_frame.pack(side=RIGHT, fill=BOTH, expand=True, padx=5, pady=5)

    # Sekcja dodawania nowych książek
    Label(book_frame, text="Dodaj nową książkę:", font=("Arial", 10, "bold")).pack(anchor=W, pady=5)

    # Lista etykiet dla pól formularza
    fields = ["Tytuł:", "Autor:", "Cena:"]
    entries = []  # Lista przechowująca referencje do wszystkich pól Entry

    # Tworzenie pól formularza w pętli
    for field in fields:
        # Ramka dla pojedynczego wiersza formularza (etykieta + pole)
        frame = Frame(book_frame)
        frame.pack(fill=X, pady=2)  # Każdy wiersz rozciąga się w poziomie

        # Etykieta pola
        Label(frame, text=field, width=8).pack(side=LEFT)

        # Pole wprowadzania danych
        entry = Entry(frame)
        entry.pack(side=LEFT, expand=True, fill=X, padx=5)
        entries.append(entry)  # Dodanie pola do listy

    # Przycisk "Dodaj książkę"
    Button(book_frame, text="Dodaj książkę",
           # Lambda wyrażenie, które:
           # 1. Tworzy listę wartości z wszystkich pól Entry (e.get())
           # 2. Rozpakowuje ją (*) jako argumenty do add_book_action
           command=lambda: add_book_action(*[e.get() for e in entries])) \
        .pack(pady=10)

    # Sekcja usuwania książek
    Label(book_frame, text="Usuń książkę:", font=("Arial", 10, "bold")).pack(anchor=W, pady=5)

    # Ramka dla elementów kontrolnych
    book_control_frame = Frame(book_frame)
    book_control_frame.pack(fill=X, pady=5)

    # Etykieta pola
    Label(book_control_frame, text="ID/Tytuł:").pack(side=LEFT, padx=5)

    # Pole wprowadzania danych
    book_delete_entry = Entry(book_control_frame, width=25)
    book_delete_entry.pack(side=LEFT, padx=5, expand=True, fill=X)

    # Przycisk "Usuń"
    Button(book_control_frame, text="Usuń",
           command=lambda: remove_book_action(book_delete_entry.get())) \
        .pack(side=LEFT, padx=5)

    # ======================================================================
    # FUNKCJE POMOCNICZE
    # ======================================================================

    def add_book_action(title, author, price):
        """
        Obsługa dodawania nowej książki do systemu.

        Parametry:
        title (str): Tytuł książki
        author (str): Autor książki
        price (str): Cena książki (jako string, który zostanie przekonwertowany na float)
        """
        # Sprawdzenie czy wszystkie pola są wypełnione
        if not all([title, author, price]):
            showinfo("Błąd", "Wszystkie pola są wymagane")
            return

        try:
            # Konwersja ceny na liczbę zmiennoprzecinkową
            price = float(price)

            # Wywołanie funkcji dodającej książkę z modułu book_Manager
            result = add_book(title, author, price)

            # Wyświetlenie komunikatu zwrotnego
            showinfo("Wynik", result["message"])

            # Jeśli operacja się powiodła (kod 200), wyczyść pola formularza
            if result["code"] == 200:
                for entry in entries:
                    entry.delete(0, END)  # Usuń tekst od znaku 0 do końca (END)
        except ValueError:
            # Obsługa błędu gdy cena nie jest liczbą
            showinfo("Błąd", "Cena musi być liczbą")

    def remove_book_action(data):
        """
        Obsługa usuwania książki z systemu.

        Parametr:
        data (str): ID lub tytuł książki do usunięcia
        """
        if not data:
            showinfo("Błąd", "Wprowadź ID lub tytuł książki")
            return

        # Wywołanie funkcji usuwającej książkę z modułu book_Manager
        result = remove_book(data)
        showinfo("Wynik", result["message"])

        # Jeśli operacja się powiodła, wyczyść pole formularza
        if result["code"] == 200:
            book_delete_entry.delete(0, END)

    def remove_user_action(data):
        """
        Obsługa usuwania użytkownika z systemu.

        Parametr:
        data (str): ID lub nazwa użytkownika do usunięcia
        """
        if not data:
            showinfo("Błąd", "Wprowadź ID lub nazwę użytkownika")
            return

        # Wywołanie funkcji usuwającej użytkownika z modułu customer_Manager
        result = remove_customer(data)
        showinfo("Wynik", result["message"])

        # Jeśli operacja się powiodła, wyczyść pole formularza
        if result["code"] == 200:
            user_delete_entry.delete(0, END)

    # Uruchomienie pętli głównej okna
    # Metoda mainloop() powoduje, że okno jest wyświetlane i czeka na interakcję użytkownika
    admin_root.mainloop()