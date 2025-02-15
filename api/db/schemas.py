from enum import Enum
from typing import Optional, OrderedDict
from pydantic import BaseModel

class Genre(str, Enum):
    """Enumeration of valid book genres."""
    SCI_FI = "Science Fiction"
    FANTASY = "Fantasy"
    HORROR = "Horror"
    MYSTERY = "Mystery"
    ROMANCE = "Romance"
    THRILLER = "Thriller"

class Book(BaseModel):
    """Pydantic model representing a book."""
    id: int
    title: str
    author: str
    publication_year: int
    genre: Genre

class InMemoryDB:
    """In-memory database implementation using OrderedDict."""
    
    def __init__(self):
        self.books: OrderedDict[int, Book] = OrderedDict()

    def get_books(self) -> OrderedDict[int, Book]:
        """Retrieve all books in insertion order."""
        return self.books

    def add_book(self, book: Book) -> Book:
        """Add a new book to the database."""
        self.books[book.id] = book  # Direct key assignment
        return book

    def get_book(self, book_id: int) -> Optional[Book]:
        """Retrieve a book by ID, returns None if not found."""
        return self.books.get(book_id)

    def update_book(self, book_id: int, data: Book) -> Book:
        """Update existing book with validation."""
        if book_id not in self.books:
            raise ValueError(f"Book ID {book_id} not found")
        self.books[book_id] = data
        return data

    def delete_book(self, book_id: int) -> None:
        """Disabled deletion method (per project requirements)."""
        raise RuntimeError("Book deletion is not allowed")