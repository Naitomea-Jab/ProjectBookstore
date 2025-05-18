# Import modułów do tworzenia GUI i okien dialogowych
from tkinter import *  # Import wszystkich klas i funkcji z biblioteki Tkinter
from tkinter.messagebox import showinfo  # Import tylko funkcji showinfo do wyświetlania komunikatów

# Import funkcji z własnych modułów
from bookstore.book_Manager import get_book  # Import funkcji do pobierania danych o książkach z backendu
from .admin_panel import start_admin_panel  # Import funkcji do uruchamiania panelu administratora

# Stałe globalne kontrolujące układ graficzny
BOOK_WIDTH = 200  # Szerokość pojedynczego widgetu książki w pikselach
MARGIN = 20  # Margines między książkami w pikselach


def create_books(books_frame, books, columns):
    """
    Funkcja tworząca dynamiczny układ książek w podanej ramce.

    Args:
        books_frame (Frame): Kontener główny dla książek
        books (list): Lista książek do wyświetlenia
        columns (int): Liczba kolumn w jakiej mają być wyświetlone książki
    """
    # 1. Czyszczenie istniejących widgetów
    for widget in books_frame.winfo_children():
        widget.destroy()  # Usuwa wszystkie istniejące elementy w ramce

    # 2. Obliczenie liczby potrzebnych wierszy
    rows = (len(books) + columns - 1) // columns  # Dzielenie z zaokrągleniem w górę

    # 3. Tworzenie wierszy z książkami
    for r in range(rows):
        # Ramka dla pojedynczego wiersza
        row_frame = Frame(books_frame)
        row_frame.pack(fill=X, pady=5)  # Rozciągnięcie w poziomie z odstępem 5px

        # 4. Dodawanie książek do wiersza
        for c in range(columns):
            index = r * columns + c  # Obliczenie indeksu książki
            if index >= len(books):  # Zabezpieczenie przed wyjściem poza zakres
                break

            book = books[index]  # Pobranie danych książki

            # 5. Tworzenie ramki dla pojedynczej książki
            frame = Frame(row_frame,
                          bd=1,  # Grubość obramowania (1px)
                          relief=GROOVE,  # Styl obramowania (wcięcie)
                          width=BOOK_WIDTH,  # Stała szerokość
                          height=100,  # Stała wysokość
                          padx=10, pady=5)  # Marginesy wewnętrzne

            frame.pack(side=LEFT, padx=5, expand=1)  # Rozmieszczenie z odstępem 5px
            frame.pack_propagate(False)  # Blokada automatycznej zmiany rozmiaru

            # 6. Dodanie tytułu książki
            Label(frame,
                  text=book[2],  # Zakładając, że tytuł jest pod indeksem 2
                  font=("Arial", 10, "bold")  # Czcionka pogrubiona
                  ).pack(anchor=W)  # Wyrównanie do lewej strony

            # 7. Dodanie autora książki
            Label(frame,
                  text=f"Autor: {book[1]}"  # Zakładając, że autor jest pod indeksem 1
                  ).pack(anchor=W)  # Wyrównanie do lewej strony

            # 8. Przycisk "Kup teraz"
            Button(frame,
                   text="Kup teraz",
                   # Lambda wyrażenie zapamiętujące tytuł książki
                   command=lambda t=book[2]: showinfo("Kupiono", f"Kupiłeś: {t}")
                   ).pack(anchor=E)  # Wyrównanie do prawej strony


def start_gui():
    """
    Główna funkcja inicjalizująca i uruchamiająca interfejs użytkownika.
    Tworzy główne okno aplikacji z dwoma panelami:
    - lewy panel: wyświetlanie książek
    - prawy panel: formularz logowania
    """
    # 1. Inicjalizacja głównego okna
    root = Tk()  # Tworzenie głównego okna aplikacji
    root.title("Sklep z książkami")  # Ustawienie tytułu okna
    root.geometry("1000x600")  # Ustawienie początkowego rozmiaru okna

    # 2. Nagłówek aplikacji
    Label(root,
          text="KSIĘGARNIA ONLINE",
          font=("Arial", 20),  # Duża czcionka
          bg="#add8e6"  # Jasnoniebieskie tło
          ).pack(fill=X, pady=10)  # Rozciągnięcie na całą szerokość z odstępem 10px

    # 3. Główny kontener dla zawartości
    main_frame = Frame(root)
    main_frame.pack(fill=BOTH, expand=1)  # Rozciągnięcie na całe dostępne miejsce

    # ==============================================================
    # LEWY PANEL - WYŚWIETLANIE KSIĄŻEK
    # ==============================================================
    books_frame = Frame(main_frame)
    books_frame.pack(side=LEFT,  # Umieszczenie z lewej strony
                     fill=BOTH,  # Wypełnienie przestrzeni
                     expand=1,  # Zezwolenie na rozszerzanie
                     padx=10)  # Odstęp od krawędzi

    # ==============================================================
    # PRAWY PANEL - LOGOWANIE
    # ==============================================================
    login_frame = Frame(main_frame,
                        bd=2,  # Grubość obramowania (2px)
                        relief=GROOVE,  # Styl obramowania
                        padx=10, pady=10,  # Marginesy wewnętrzne
                        bg="#f0f0f0"  # Jasnoszare tło
                        )
    login_frame.pack(side=RIGHT,  # Umieszczenie z prawej strony
                     fill=Y,  # Wypełnienie tylko w pionie
                     padx=10, pady=10)  # Odstępy od krawędzi

    # 4. Formularz logowania
    # Tytuł sekcji
    Label(login_frame,
          text="Logowanie",
          font=("Arial", 12, "bold"),  # Pogrubiona czcionka
          bg="#f0f0f0"  # Kolor tła zgodny z ramką
          ).grid(row=0, columnspan=2, pady=5)  # Rozciągnięcie na 2 kolumny

    # Pole login
    Label(login_frame,
          text="Login:",
          bg="#f0f0f0"
          ).grid(row=1, column=0, sticky=W, pady=2)  # Wyrównanie do lewej
    Entry(login_frame).grid(row=1, column=1, pady=2)  # Pole wprowadzania tekstu

    # Pole hasło
    Label(login_frame,
          text="Hasło:",
          bg="#f0f0f0"
          ).grid(row=2, column=0, sticky=W, pady=2)  # Wyrównanie do lewej
    Entry(login_frame,
          show="*"  # Maskowanie znaków (gwiazdki zamiast tekstu)
          ).grid(row=2, column=1, pady=2)

    # Przycisk logowania
    Button(login_frame,
           text="Zaloguj",
           # Wyświetlenie komunikatu po kliknięciu
           command=lambda: showinfo("Info", "Funkcja logowania")
           ).grid(row=3, columnspan=2, pady=5)  # Rozciągnięcie na 2 kolumny

    # Przycisk "Zarządzaj" (panel administratora)
    Button(login_frame,
           text="Zarządzaj",
           command=start_admin_panel  # Uruchomienie panelu admina
           ).grid(row=4, columnspan=2, pady=10)  # Większy odstęp pionowy

    # 5. Pobranie danych o książkach z backendu
    result = get_book()
    if result["code"] != 200:  # Jeśli wystąpił błąd
        # Wyświetlenie komunikatu o błędzie
        Label(books_frame,
              text=result["message"],
              fg="red"  # Czerwony kolor tekstu
              ).pack()
        root.mainloop()  # Uruchomienie pętli głównej
        return  # Zakończenie funkcji

    books = result["data"]  # Lista książek
    last_columns = [0]  # Śledzenie ostatniej liczby kolumn (jako lista aby była mutowalna)

    def safe_resize(event):
        """
        Funkcja dostosowująca układ książek do aktualnego rozmiaru okna.
        Wywoływana przy każdej zmianie rozmiaru okna.
        """
        try:
            # 1. Pobranie aktualnej szerokości obszaru książek
            width = books_frame.winfo_width()
            if width < 1:  # Zabezpieczenie przed błędami
                return

            # 2. Obliczenie optymalnej liczby kolumn
            columns = max(1, width // (BOOK_WIDTH + MARGIN))

            # 3. Aktualizacja tylko jeśli liczba kolumn się zmieniła
            if columns != last_columns[0]:
                last_columns[0] = columns  # Zapisanie nowej wartości
                create_books(books_frame, books, columns)  # Przerysowanie książek
        except Exception as e:
            print("Resize error:", e)  # Logowanie błędów w konsoli

    # 6. Powiązanie zdarzenia zmiany rozmiaru okna z funkcją
    root.bind("<Configure>", safe_resize)

    # 7. Początkowe wywołanie funkcji resize po 100ms
    root.after(100, lambda: safe_resize(None))

    # 8. Uruchomienie pętli głównej aplikacji
    root.mainloop()


if __name__ == "__main__":
    # Uruchomienie aplikacji jeśli plik jest wykonywany bezpośrednio
    start_gui()