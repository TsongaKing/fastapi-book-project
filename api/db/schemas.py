from typing import Optional, OrderedDict  # Add this at the top
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

    def get_book(self, book_id: int) -> Optional[Book]:  # Now valid
        return self.books.get(book_id)
    
    def update_book(self, book_id: int, data: Book) -> Book:
        if book_id not in self.books:
            raise ValueError(f"Book ID {book_id} not found")
        self.books[book_id] = data
        return data

    def delete_book(self, book_id: int) -> None:
        raise RuntimeError("Book deletion is not allowed")