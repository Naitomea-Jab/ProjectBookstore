# API Dokumentacja

## Funkcja `get_book`

### Opis
Funkcja `get_book` pobiera książki z bazy danych. Można pobrać wszystkie książki, książki o określonym ID lub książki o określonym tytule.

### Argumenty
- **data** (*str, opcjonalny*): ID książki (jako string) lub tytuł książki (jako string). Jeśli brak argumentu (domyślnie `None`), funkcja zwróci wszystkie książki.

### Zwracane wartości
Funkcja zwraca słownik z danymi o książkach w następującym formacie:

- **code** (*int*): Kod HTTP. 
  - `200` – jeśli książki zostały znalezione,
  - `404` – jeśli brak wyników.
  
- **message** (*str*): Komunikat o wyniku operacji (np. "OK" lub "Nie znaleziono książki do wypisania").
  
- **data** (*list*, jeśli `code = 200`): Lista krotek zawierających dane o książkach. Każda krotka zawiera:
  - **ID** (*int*): ID książki.
  - **AUTHOR** (*str*): Autor książki.
  - **TITLE** (*str*): Tytuł książki.
  - **NO_EBOOK_AVAILABLE** (*int*): Liczba dostępnych egzemplarzy.
  - **CREATED** (*str*): Data utworzenia książki.
  - **UPDATED** (*str*): Data ostatniej aktualizacji książki.

### Przykład użycia

#### Pobranie wszystkich książek:
```python
result = get_book()
if result["code"] == 200:
    for book in result["data"]:
        print(book)
```

#### Pobranie książki o określonym ID:
```python
result = get_book("5")
if result["code"] == 200:
    for book in result["data"]:
        print(book)
```

#### Pobranie książki o określonym tytule:
```python
result = get_book("Władca Pierścieni")
if result["code"] == 200:
    for book in result["data"]:
        print(book)
```

## Funkcja `add_book`

### Opis
Funkcja `add_book` dodaje nową książkę do bazy danych.

### Argumenty
- **bookInfo** (*list*): Lista zawierająca informacje o książce w następującej kolejności:
  - **author** (*str*): Imię i nazwisko autora.
  - **title** (*str*): Tytuł książki.
  - **amount** (*int*): Liczba dostępnych egzemplarzy (musi być >= 0).

### Zwracane wartości
Funkcja zwraca słownik zawierający:

- **code** (*int*): Kod HTTP-stylu.
  - `201` – jeśli książka została pomyślnie dodana,
  - `400` – jeśli podano niepoprawną ilość egzemplarzy.

- **message** (*str*): Komunikat informujący o wyniku operacji.

### Przykład użycia
```python
new_book = ["J.K. Rowling", "Harry Potter i Kamień Filozoficzny", 10]
result = add_book(new_book)
print(result["code"])
```

## Funkcja `remove_book`

### Opis
Funkcja `remove_book` usuwa książkę z bazy danych na podstawie ID lub tytułu.

### Argumenty
- **data** (*str*): ID książki (liczba całkowita jako string) lub tytuł (string) książki do usunięcia.

### Zwracane wartości
Funkcja zwraca słownik zawierający:

- **code** (*int*): Kod HTTP-stylu.
  - `200` – jeśli usunięto książkę,
  - `404` – jeśli nie znaleziono książki do usunięcia.

- **message** (*str*): Komunikat opisujący wynik operacji.

### Przykład użycia

#### Usunięcie książki po ID:
```python
result = remove_book("5")
print(result["code"])
```

#### Usunięcie książki po tytule:
```python
result = remove_book("Harry Potter i Kamień Filozoficzny")
print(result["code"])
```