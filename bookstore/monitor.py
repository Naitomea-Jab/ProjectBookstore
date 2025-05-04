# monitor.py
from datetime import datetime
from bookstore.utilities import FILE_DIR
from bookstore.book_Manager import get_book
import os
import re
from collections import Counter

def get_total_books(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM book")
    return {
        "code": 200,
        "message": "OK",
        "data": cursor.fetchall()[0][0]
    }

def get_books_by_author(conn, author):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM book WHERE author = ?", (author,))
    return {
        "code": 200,
        "message": "OK",
        "data": cursor.fetchall()
    }

def get_ebooks_unavailable(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM book WHERE NO_EBOOK_AVAILABLE < 1")
    return {
        "code": 200,
        "message": "OK",
        "data": cursor.fetchall()
    }

def get_total_customers(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM customer")
    return {
        "code": 200,
        "message": "OK",
        "data": cursor.fetchall()[0][0]
    }

def get_total_purchases(conn, customer_data):
    filename = f"{customer_data}.txt"
    file_path = os.path.join(FILE_DIR, filename)
    with open(file_path, 'r') as file:
        line_count = sum(1 for line in file)
    return {
        "code": 200,
        "message": "OK",
        "data": line_count
    }

def get_most_popular_books(conn, amount=3):
    cursor = conn.cursor()
    book_counter = Counter()
    #Get list of all ID's from all files, then count them using counter
    for filename in os.listdir(FILE_DIR):
        if filename.endswith('.txt'):
            file_path = os.path.join(FILE_DIR, filename)
            book_ids = []
            pattern = r"BookID:\s*(\d+)"

            with open(file_path, 'r') as file:
                content = file.read()
                book_ids = re.findall(pattern, content)

            book_counter.update(book_ids)

    sorted_books = book_counter.most_common(amount)
    final_results = []

    for i in range(amount):
        book_id = sorted_books[i][0]
        cursor.execute("SELECT * FROM book WHERE ID = ?", (book_id,))
        result = cursor.fetchone()
        if result:
            result_with_number = result + (sorted_books[i][1],)
            final_results.append(result_with_number)

    return {
        "code": 200,
        "message": "OK",
        "data": final_results
    }

def get_newest_books(conn, last_n_days=30):
    current_date = datetime.now()
    result = get_book()
    books_newer_than_n = []
    for book in result["data"]:
        book_creation_time = datetime.strptime(book[4], "%Y-%m-%d")
        diff = current_date - book_creation_time
        if diff.days < last_n_days:
            books_newer_than_n.append(book)
    return {
        "code": 200,
        "message": "OK",
        "data": tuple(books_newer_than_n)
    }

def get_customer_countries(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*), COUNTRY FROM address GROUP BY COUNTRY ORDER BY COUNT(*) DESC")
    return {
        "code": 200,
        "message": "OK",
        "data": cursor.fetchall()
    }
