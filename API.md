# Dokumentacja API Systemu Księgarni

## Spis treści
1. [Zarządzanie Książkami](#zarządzanie-książkami)
2. [Zarządzanie Klientami](#zarządzanie-klientami)
3. [Monitorowanie i Statystyki](#monitorowanie-i-statystyki)
4. [Zarządzanie Plikami](#zarządzanie-plikami)
5. [Narzędzia Pomocnicze](#narzędzia-pomocnicze)
6. [Struktury Danych](#struktury-danych)
7. [Kody Odpowiedzi](#kody-odpowiedzi)

---

## Zarządzanie Książkami

### `get_book(data=None)`
**Opis:** Pobiera książki z bazy danych.

**Parametry:**
- `data` (str, optional): ID książki lub tytuł książki. Jeśli None, pobiera wszystkie książki.

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 404 (brak wyników), 500 (błąd)
    "message": str,       # Komunikat o wyniku operacji
    "data": list          # Lista krotek z danymi książek (tylko przy code=200)
}
```

**Struktura danych książki:**
```
(BookID, Title, Author, Genre, Price, Stock, DateAdded)
```

**Przykłady użycia:**
```python
# Wszystkie książki
get_book()

# Książka po ID
get_book("1")

# Książki po tytule (częściowe dopasowanie)
get_book("Harry Potter")
```

---

### `add_book(bookInfo)`
**Opis:** Dodaje nową książkę do bazy danych. Funkcja jest ozdobiona dekoratorem `@log_performance`.

**Parametry:**
- `bookInfo` (dict): Słownik z informacjami o książce

**Wymagane pola w `bookInfo`:**
```python
{
    "Title": str,      # Tytuł książki
    "Author": str,     # Autor książki
    "Genre": str,      # Gatunek książki (opcjonalnie)
    "Price": float,    # Cena książki (≥ 0)
    "Stock": int       # Stan magazynowy (≥ 0)
}
```

**Zwraca:**
```python
{
    "code": int,          # 201 (sukces), 400 (błąd walidacji), 409 (konflikt), 500 (błąd bazy)
    "message": str        # Komunikat o wyniku operacji
}
```

---

### `remove_book(data)`
**Opis:** Usuwa książkę z bazy danych.

**Parametry:**
- `data` (str): ID książki lub tytuł książki

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 404 (nie znaleziono), 500 (błąd bazy)
    "message": str        # Komunikat o wyniku operacji
}
```

---

### `update_book_stock(book_id, quantity_change)`
**Opis:** Aktualizuje stan magazynowy książki.

**Parametry:**
- `book_id` (int): ID książki
- `quantity_change` (int): Zmiana ilości (może być ujemna)

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 400 (błąd walidacji), 404 (nie znaleziono), 500 (błąd bazy)
    "message": str        # Komunikat o wyniku operacji
}
```

---

## Zarządzanie Klientami

### `get_customers(data=None)`
**Opis:** Pobiera klientów z bazy danych.

**Parametry:**
- `data` (str, optional): ID klienta (UUID format) lub imię i nazwisko. Jeśli None, pobiera wszystkich klientów.

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 404 (brak wyników), 500 (błąd)
    "message": str,       # Komunikat o wyniku operacji
    "data": list          # Lista krotek z danymi klientów (tylko przy code=200)
}
```

**Struktura danych klienta:**
```
(CustomerID, Name, Email)
```

---

### `register_customer(clientInfo)`
**Opis:** Rejestruje nowego klienta w bazie danych.

**Parametry:**
- `clientInfo` (dict): Słownik z informacjami o kliencie

**Wymagane pola w `clientInfo`:**
```python
{
    "Name": str,       # Imię i nazwisko klienta
    "Email": str       # Adres email klienta (unikalny)
}
```

**Zwraca:**
```python
{
    "code": int,          # 201 (sukces), 400 (błąd walidacji), 409 (konflikt), 500 (błąd bazy)
    "message": str        # Komunikat zawierający ID nowego klienta
}
```

---

### `remove_customer(data)`
**Opis:** Usuwa klienta z bazy danych wraz z jego zakupami (transakcja atomowa).

**Parametry:**
- `data` (str): ID klienta (UUID) lub imię i nazwisko

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 404 (nie znaleziono), 500 (błąd bazy)
    "message": str        # Komunikat o liczbie usuniętych rekordów
}
```

---

### `buy_book(customer_data, book_data, quantity)`
**Opis:** Obsługuje proces zakupu książki (transakcja atomowa).

**Parametry:**
- `customer_data` (str): ID klienta lub imię i nazwisko
- `book_data` (str): ID książki lub tytuł książki
- `quantity` (int): Liczba kupowanych książek

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 400 (błąd walidacji), 404 (nie znaleziono), 500 (błąd bazy)
    "message": str        # Komunikat o wyniku operacji
}
```

**Walidacja:**
- Sprawdza dostępność książki w magazynie
- Automatycznie aktualizuje stan magazynowy
- Zapisuje transakcję z aktualną datą

---

### `get_customer_purchases(customer_data)`
**Opis:** Pobiera historię zakupów dla konkretnego klienta.

**Parametry:**
- `customer_data` (str): ID klienta lub imię i nazwisko

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 404 (nie znaleziono), 500 (błąd bazy)
    "message": str,       # Komunikat o wyniku operacji
    "data": list          # Lista krotek z danymi zakupów (tylko przy code=200)
}
```

**Struktura danych zakupu:**
```
(PurchaseID, CustomerName, BookTitle, Quantity, PurchaseDate, BookPrice)
```

---

## Monitorowanie i Statystyki

### `get_total_books()`
**Opis:** Zwraca całkowitą liczbę książek w bazie danych.

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 500 (błąd bazy)
    "message": str,       # Komunikat o wyniku operacji
    "data": int           # Liczba książek
}
```

---

### `get_books_by_author(author)`
**Opis:** Zwraca wszystkie książki danego autora.

**Parametry:**
- `author` (str): Nazwa autora

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 404 (brak wyników), 500 (błąd bazy)
    "message": str,       # Komunikat o wyniku operacji
    "data": list          # Lista krotek z danymi książek
}
```

---

### `get_ebooks_unavailable()`
**Opis:** Zwraca liczbę książek niedostępnych w magazynie (stock = 0).

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 500 (błąd bazy)
    "message": str,       # Komunikat o wyniku operacji
    "data": int           # Liczba niedostępnych książek
}
```

---

### `get_total_customers()`
**Opis:** Zwraca całkowitą liczbę klientów.

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 500 (błąd bazy)
    "message": str,       # Komunikat o wyniku operacji
    "data": int           # Liczba klientów
}
```

---

### `get_total_purchases()`
**Opis:** Zwraca całkowitą liczbę zakupów.

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 500 (błąd bazy)
    "message": str,       # Komunikat o wyniku operacji
    "data": int           # Liczba zakupów
}
```

---

### `get_popular_books(limit=5)`
**Opis:** Zwraca najpopularniejsze książki na podstawie liczby sprzedanych egzemplarzy.

**Parametry:**
- `limit` (int, optional): Maksymalna liczba zwracanych książek (domyślnie 5)

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 404 (brak danych), 500 (błąd bazy)
    "message": str,       # Komunikat o wyniku operacji
    "data": list          # Lista krotek (Title, Author, TotalQuantitySold)
}
```

---

### `get_recent_books(limit=5)`
**Opis:** Zwraca ostatnio dodane książki.

**Parametry:**
- `limit` (int, optional): Maksymalna liczba zwracanych książek (domyślnie 5)

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 404 (brak danych), 500 (błąd bazy)
    "message": str,       # Komunikat o wyniku operacji
    "data": list          # Lista krotek (BookID, Title, Author, DateAdded)
}
```

---

### `get_books_by_genre(genre)`
**Opis:** Zwraca wszystkie książki danego gatunku (częściowe dopasowanie).

**Parametry:**
- `genre` (str): Nazwa gatunku

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 404 (brak wyników), 500 (błąd bazy)
    "message": str,       # Komunikat o wyniku operacji
    "data": list          # Lista krotek z pełnymi danymi książek
}
```

---

### `get_revenue_statistics()`
**Opis:** Zwraca statystyki przychodów.

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 500 (błąd bazy)
    "message": str,       # Komunikat o wyniku operacji
    "data": {
        "total_revenue": float,     # Całkowity przychód
        "monthly_revenue": float    # Przychód z ostatnich 30 dni
    }
}
```

---

### `get_low_stock_books(threshold=10)`
**Opis:** Zwraca książki z niskim stanem magazynowym.

**Parametry:**
- `threshold` (int, optional): Próg niskiego stanu (domyślnie 10)

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 404 (brak wyników), 500 (błąd bazy)
    "message": str,       # Komunikat o wyniku operacji
    "data": list          # Lista krotek (BookID, Title, Author, Stock)
}
```

---

### `get_purchase_history(start_date=None, end_date=None)`
**Opis:** Zwraca historię zakupów z opcjonalnym filtrem dat.

**Parametry:**
- `start_date` (str, optional): Data początkowa (format: YYYY-MM-DD)
- `end_date` (str, optional): Data końcowa (format: YYYY-MM-DD)

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 404 (brak danych), 500 (błąd bazy)
    "message": str,       # Komunikat o wyniku operacji
    "data": list          # Lista krotek (PurchaseID, CustomerName, BookTitle, Quantity, PurchaseDate, TotalPrice)
}
```

**Uwaga:** Bez filtra dat zwraca maksymalnie 100 ostatnich zakupów.

---

## Zarządzanie Plikami

### `export_data(table_name, filename=None)`
**Opis:** Eksportuje dane z podanej tabeli do pliku CSV w folderze DATABASE.

**Parametry:**
- `table_name` (str): Nazwa tabeli ('Customers', 'Books', 'Purchases')
- `filename` (str, optional): Nazwa pliku CSV (domyślnie: 'nazwa_tabeli.csv')

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 404 (błąd bazy), 500 (błąd ogólny)
    "message": str        # Komunikat z ścieżką pliku lub błędem
}
```

---

### `import_data(table_name, filename=None)`
**Opis:** Importuje dane z pliku CSV z folderu DATABASE do podanej tabeli.

**Parametry:**
- `table_name` (str): Nazwa tabeli ('Customers', 'Books', 'Purchases')
- `filename` (str, optional): Nazwa pliku CSV (domyślnie: 'nazwa_tabeli.csv')

**Zwraca:**
```python
{
    "code": int,          # 200 (sukces), 400 (błąd walidacji), 404 (brak pliku), 500 (błąd ogólny)
    "message": str        # Komunikat o wyniku operacji
}
```

**Wymagane kolumny CSV:**

**Customers:**
- CustomerID, Name, Email

**Books:**
- Title, Author, Genre, Price, Stock, DateAdded

**Purchases:**
- CustomerID, BookID, Quantity, PurchaseDate

**Uwagi dotyczące importu:**
- Duplikaty email w Customers są pomijane z ostrzeżeniem
- Książki z tym samym tytułem i autorem są aktualizowane
- Zakupy z nieistniejącymi CustomerID/BookID są pomijane
- Nieprawidłowe daty są zastępowane bieżącą datą

---

## Narzędzia Pomocnicze

### `generate_customer_id()`
**Opis:** Generuje unikalny UUID dla nowego klienta.

**Zwraca:**
- `str`: Unikalny identyfikator UUID w formacie string

---

### `validate_email(email)`
**Opis:** Podstawowa walidacja adresu email.

**Parametry:**
- `email` (str): Adres email do walidacji

**Zwraca:**
- `bool`: True jeśli email jest poprawny, False w przeciwnym razie

**Wzorzec walidacji:**
```regex
^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$
```

---

### `initialize_database()`
**Opis:** Inicjalizuje bazę danych: tworzy folder DATABASE, plik bazy danych i tabele jeśli nie istnieją.

**Tworzone tabele:**
- **Customers**: CustomerID (TEXT, PK), Name (TEXT), Email (TEXT, UNIQUE)
- **Books**: BookID (INTEGER, PK, AUTOINCREMENT), Title, Author, Genre, Price, Stock, DateAdded
- **Purchases**: PurchaseID (INTEGER, PK, AUTOINCREMENT), CustomerID (FK), BookID (FK), Quantity, PurchaseDate

---

### `log_performance(func)` (Dekorator)
**Opis:** Dekorator logujący czas wykonania funkcji. Używany z funkcją `add_book()`.

**Działanie:**
- Mierzy czas wykonania funkcji
- Wypisuje komunikat z czasem wykonania w sekundach
- Zwraca oryginalny wynik funkcji

---

## Struktury Danych

### Książka (Books)
```python
(
    BookID: int,           # Unikalny identyfikator (auto-increment)
    Title: str,            # Tytuł książki
    Author: str,           # Autor książki
    Genre: str,            # Gatunek książki
    Price: float,          # Cena książki
    Stock: int,            # Stan magazynowy
    DateAdded: str         # Data dodania (YYYY-MM-DD HH:MM:SS)
)
```

### Klient (Customers)
```python
(
    CustomerID: str,       # Unikalny UUID
    Name: str,             # Imię i nazwisko
    Email: str             # Adres email (unikalny)
)
```

### Zakup (Purchases)
```python
(
    PurchaseID: int,       # Unikalny identyfikator (auto-increment)
    CustomerID: str,       # ID klienta (FK)
    BookID: int,           # ID książki (FK)
    Quantity: int,         # Liczba kupowanych egzemplarzy
    PurchaseDate: str      # Data zakupu (YYYY-MM-DD HH:MM:SS)
)
```

---

## Kody Odpowiedzi

| Kod | Znaczenie | Opis |
|-----|-----------|------|
| 200 | OK | Operacja zakończona sukcesem |
| 201 | Created | Nowy rekord został utworzony |
| 400 | Bad Request | Błąd walidacji danych wejściowych |
| 404 | Not Found | Nie znaleziono wymaganych danych |
| 409 | Conflict | Konflikt danych (np. duplikat email) |
| 500 | Internal Server Error | Błąd bazy danych lub nieoczekiwany błąd |

---

## Konfiguracja Ścieżek

```python
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
FILE_DIR = os.path.join(BASE_DIR, "DATABASE")
DB_PATH = os.path.join(BASE_DIR, "DATABASE", "bookstore_main.db")
```

**Struktura folderów:**
```
projekt/
├── DATABASE/
│   ├── bookstore_main.db
│   ├── customers.csv
│   ├── books.csv
│   └── purchases.csv
└── bookstore/
    ├── book_Manager.py
    ├── customer_Manager.py
    ├── monitor.py
    ├── file_manager.py
    └── utilities.py
```

---

## Obsługa Błędów

Wszystkie funkcje implementują obsługę błędów zgodnie z następującym wzorcem:

1. **Połączenie z bazą danych** - w bloku try-finally z automatycznym zamykaniem połączenia
2. **Walidacja danych wejściowych** - sprawdzanie wymaganych pól i typów danych
3. **Transakcje atomowe** - dla operacji modyfikujących wiele tabel (usuwanie klienta, zakup książki)
4. **Rollback** - w przypadku błędów podczas transakcji
5. **Szczegółowe komunikaty błędów** - ułatwiające debugowanie

Przykład struktury odpowiedzi błędu:
```python
{
    "code": 500,
    "message": "Błąd bazy danych podczas operacji: szczegóły błędu"
}
```