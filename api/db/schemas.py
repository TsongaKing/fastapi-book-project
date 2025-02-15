from typing import Optional, OrderedDict
from enum import Enum
from pydantic import BaseModel

class Genre(str, Enum):
    SCI_FI = "Science Fiction"
    FANTASY = "Fantasy"
    HORROR = "Horror"
    MYSTERY = "Mystery"
    ROMANCE = "Romance"
    THRILLER = "Thriller"

class Book(BaseModel):
    id: int
    title: str
    author: str
    publication_year: int
    genre: Genre

class InMemoryDB:
    def __init__(self):
        self.books: OrderedDict[int, Book] = OrderedDict()

    def get_books(self) -> OrderedDict[int, Book]:  # Added this method
        return self.books

    def get_book(self, book_id: int) -> Optional[Book]:
        return self.books.get(book_id)
    
    def add_book(self, book: Book) -> Book:  # Added this method
        if book.id in self.books:
            raise ValueError(f"Book ID {book.id} already exists")
        self.books[book.id] = book
        return book
    
    def update_book(self, book_id: int, data: Book) -> Book:
        if book_id not in self.books:
            raise ValueError(f"Book ID {book_id} not found")
        self.books[book_id] = data
        return data

    def delete_book(self, book_id: int) -> None:
        raise RuntimeError("Book deletion is not allowed")