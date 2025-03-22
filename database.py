import sqlite3
from sqlite3 import Error

def create_connection():
    return sqlite3.connect('books.db', check_same_thread=False)

def initialize_database():
    commands = [
        '''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT,
            isbn TEXT UNIQUE,
            stock INTEGER DEFAULT 1
        );''',
        '''CREATE TABLE IF NOT EXISTS borrowed (
            id INTEGER PRIMARY KEY,
            book_id INTEGER,
            borrower_name TEXT,
            due_date TEXT,
            FOREIGN KEY (book_id) REFERENCES books (id)
        );'''
    ]
    
    conn = create_connection()
    with conn:
        for cmd in commands:
            conn.execute(cmd)
        conn.commit()

def add_sample_data():
    books = [
        ("The Great Gatsby", "F. Scott Fitzgerald", "Classic", "9780743273565", 5),
        ("1984", "George Orwell", "Dystopian", "9780451524935", 3),
        ("The Hobbit", "J.R.R. Tolkien", "Fantasy", "9780547928227", 2),
        ("To Kill a Mockingbird", "Harper Lee", "Fiction", "9780446310789", 4)
    ]
    
    conn = create_connection()
    with conn:
        conn.executemany('''INSERT INTO books (title, author, genre, isbn, stock)
                        VALUES (?, ?, ?, ?, ?)''', books)
        conn.commit()

if __name__ == "__main__":
    initialize_database()
    add_sample_data()