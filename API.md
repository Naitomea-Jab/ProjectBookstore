# API Dokumentacja

## Spis treści
- [Zarządzanie książkami](#zarządzanie-książkami)
  - [get_book](#funkcja-get_book)
  - [add_book](#funkcja-add_book)
  - [remove_book](#funkcja-remove_book)
- [Zarządzanie klientami](#zarządzanie-klientami)
  - [get_customers](#funkcja-get_customers)
  - [get_addresses](#funkcja-get_addresses)
  - [register_customer](#funkcja-register_customer)
  - [remove_customer](#funkcja-remove_customer)
  - [buy_book](#funkcja-buy_book)

## Zarządzanie książkami

### Funkcja `get_book`

#### Opis
Funkcja `get_book` pobiera książki z bazy danych. Można pobrać wszystkie książki, książki o określonym ID lub książki o określonym tytule.

#### Argumenty
- **data** (*str, opcjonalny*): ID książki (jako string) lub tytuł książki (jako string). Jeśli brak argumentu (domyślnie `None`), funkcja zwróci wszystkie książki.

#### Zwracane wartości
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

#### Przykład użycia

##### Pobranie wszystkich książek:
```python
result = get_book()
if result["code"] == 200:
    for book in result["data"]:
        print(book)
```

##### Pobranie książki o określonym ID:
```python
result = get_book("5")
if result["code"] == 200:
    for book in result["data"]:
        print(book)
```

##### Pobranie książki o określonym tytule:
```python
result = get_book("Władca Pierścieni")
if result["code"] == 200:
    for book in result["data"]:
        print(book)
```

### Funkcja `add_book`

#### Opis
Funkcja `add_book` dodaje nową książkę do bazy danych.

#### Argumenty
- **bookInfo** (*list*): Lista zawierająca informacje o książce w następującej kolejności:
  - **author** (*str*): Imię i nazwisko autora.
  - **title** (*str*): Tytuł książki.
  - **amount** (*int*): Liczba dostępnych egzemplarzy (musi być >= 0).

#### Zwracane wartości
Funkcja zwraca słownik zawierający:

- **code** (*int*): Kod HTTP-stylu.
  - `201` – jeśli książka została pomyślnie dodana,
  - `400` – jeśli podano niepoprawną ilość egzemplarzy.

- **message** (*str*): Komunikat informujący o wyniku operacji.

#### Przykład użycia
```python
new_book = ["J.K. Rowling", "Harry Potter i Kamień Filozoficzny", 10]
result = add_book(new_book)
print(result["code"])
```

### Funkcja `remove_book`

#### Opis
Funkcja `remove_book` usuwa książkę z bazy danych na podstawie ID lub tytułu.

#### Argumenty
- **data** (*str*): ID książki (liczba całkowita jako string) lub tytuł (string) książki do usunięcia.

#### Zwracane wartości
Funkcja zwraca słownik zawierający:

- **code** (*int*): Kod HTTP-stylu.
  - `200` – jeśli usunięto książkę,
  - `404` – jeśli nie znaleziono książki do usunięcia.

- **message** (*str*): Komunikat opisujący wynik operacji.

#### Przykład użycia

##### Usunięcie książki po ID:
```python
result = remove_book("5")
print(result["code"])
```

##### Usunięcie książki po tytule:
```python
result = remove_book("Harry Potter i Kamień Filozoficzny")
print(result["code"])
```

## Zarządzanie klientami

### Funkcja `get_customers`

#### Opis
Pobiera klientów z bazy danych. Można pobrać wszystkich klientów, klientów o określonym ID lub klientów o określonym imieniu i nazwisku.

#### Argumenty
- **data** (*str, opcjonalny*): ID klienta (jako string) lub imię i nazwisko klienta (jako string). Jeśli brak argumentu (domyślnie `None`), pobierani są wszyscy klienci.

#### Zwracane wartości
Funkcja zwraca słownik zawierający:

- **code** (*int*): Kod HTTP.
  - `200` – jeśli klienci zostali znalezieni,
  - `404` – jeśli brak wyników.

- **message** (*str*): Komunikat o wyniku operacji (np. "OK" lub "Nie znaleziono klienta do wypisania").

- **data** (*list*, jeżeli `code = 200`): Lista krotek zawierających dane o klientach. Każda krotka zawiera:
  - **ID** (*int*): ID klienta.
  - **NAME** (*str*): Imię i nazwisko klienta.
  - **E-MAIL** (*str*): Adres email klienta.
  - **PHONE** (*str*): Numer telefonu klienta.
  - **CREATED** (*str*): Data utworzenia klienta.
  - **UPDATED** (*str*): Data ostatniej aktualizacji klienta.

#### Przykład użycia

##### Pobranie wszystkich klientów:
```python
result = get_customers()
if result["code"] == 200:
    for customer in result["data"]:
        print(customer)
```

##### Pobranie klienta o określonym ID:
```python
result = get_customers("5")
if result["code"] == 200:
    for customer in result["data"]:
        print(customer)
```

##### Pobranie klienta o określonym imieniu i nazwisku:
```python
result = get_customers("Jan Kowalski")
if result["code"] == 200:
    for customer in result["data"]:
        print(customer)
```

### Funkcja `get_addresses`

#### Opis
Pobiera adresy klientów z bazy danych. Można pobrać wszystkie adresy, adres dla określonego ID klienta lub adres dla klienta o określonym imieniu i nazwisku.

#### Argumenty
- **data** (*str, opcjonalny*): ID klienta (jako string) lub imię i nazwisko klienta (jako string). Jeśli brak argumentu (domyślnie `None`), pobierane są wszystkie adresy.

#### Zwracane wartości
Funkcja zwraca słownik zawierający:

- **code** (*int*): Kod HTTP.
  - `200` – jeśli adresy zostały znalezione,
  - `404` – jeśli brak wyników.

- **message** (*str*): Komunikat o wyniku operacji (np. "OK" lub "Nie znaleziono adresu do wypisania").

- **data** (*list*, jeżeli `code = 200`): Lista krotek zawierających dane o adresach. Każda krotka zawiera:
  - **ID** (*int*): ID klienta, do którego należy adres.
  - **STREET** (*str*): Nazwa ulicy.
  - **CITY** (*str*): Nazwa miasta.
  - **COUNTRY** (*str*): Nazwa kraju.

#### Przykład użycia

##### Pobranie wszystkich adresów:
```python
result = get_addresses()
if result["code"] == 200:
    for address in result["data"]:
        print(address)
```

##### Pobranie adresu dla określonego ID klienta:
```python
result = get_addresses("5")
if result["code"] == 200:
    for address in result["data"]:
        print(address)
```

##### Pobranie adresu dla klienta o określonym imieniu i nazwisku:
```python
result = get_addresses("Jan Kowalski")
if result["code"] == 200:
    for address in result["data"]:
        print(address)
```

### Funkcja `register_customer`

#### Opis
Rejestruje nowego klienta w bazie danych wraz z jego adresem.

#### Argumenty
- **clientInfo** (*list*): Lista zawierająca informacje o kliencie w kolejności:
  - **name** (*str*): Imię i nazwisko klienta.
  - **email** (*str*): Adres email klienta.
  - **phone** (*str*): Numer telefonu klienta.
- **addressInfo** (*list*): Lista zawierająca informacje o adresie klienta w kolejności:
  - **street** (*str*): Nazwa ulicy.
  - **city** (*str*): Nazwa miasta.
  - **country** (*str*): Nazwa kraju.

#### Zwracane wartości
Funkcja zwraca słownik zawierający:

- **code** (*int*): Kod HTTP-stylu. `201` jeśli klient został zarejestrowany pomyślnie.
- **message** (*str*): Komunikat informujący o wyniku operacji.

#### Przykład użycia
```python
client_info = ["Jan Kowalski", "jan@example.com", "123456789"]
address_info = ["ul. Kwiatowa 5", "Warszawa", "Polska"]
result = register_customer(client_info, address_info)
print(result["code"])
```

### Funkcja `remove_customer`

#### Opis
Usuwa klienta i jego adres z bazy danych na podstawie ID lub imienia i nazwiska.

#### Argumenty
- **data** (*str*): ID klienta (liczba całkowita jako string) lub imię i nazwisko klienta (string) do usunięcia.

#### Zwracane wartości
Funkcja zwraca słownik zawierający:

- **code** (*int*): Kod HTTP-stylu.
  - `200` – jeśli usunięto klienta,
  - `404` – jeśli nie znaleziono klienta do usunięcia.

- **message** (*str*): Komunikat opisujący wynik operacji.

#### Przykład użycia

##### Usunięcie klienta po ID:
```python
result = remove_customer("5")
print(result["code"])
```

##### Usunięcie klienta po imieniu i nazwisku:
```python
result = remove_customer("Jan Kowalski")
print(result["code"])
```

### Funkcja `buy_book`

#### Opis
Zakup książki przez klienta, zapisując informację o zakupie do pliku tekstowego klienta.

#### Argumenty
- **client_id** (*int*): ID klienta dokonującego zakupu.
- **book_data** (*list*): Lista zawierająca dane o książce (powinna zawierać ID i tytuł na indeksach 0 i 2).
- **duration** (*str*): Czas trwania dostępu do książki w miesiącach (jako string).

#### Zwracane wartości
Funkcja zwraca słownik zawierający:

- **code** (*int*): Kod HTTP-stylu. `200` jeśli zakup został zarejestrowany pomyślnie.
- **message** (*str*): Komunikat informujący o wyniku operacji.

#### Przykład użycia
```python
# Pobierz dane książki
book_result = get_book("5")
if book_result["code"] == 200:
    book_data = book_result["data"][0]
    # Przeprowadź zakup
    result = buy_book(3, book_data, "6")
    print(result["code"])
```