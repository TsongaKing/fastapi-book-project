
from typing import OrderedDict
from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse
from api.db.schemas import Book, Genre, InMemoryDB

router = APIRouter(tags=["books"], prefix="/api/v1")

db = InMemoryDB()
db.books = {
    1: Book(
        id=1,
        title="The Hobbit",
        author="J.R.R. Tolkien",
        publication_year=1937,
        genre=Genre.SCI_FI,
    ),
    2: Book(
        id=2,
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        publication_year=1954,
        genre=Genre.FANTASY,
    ),
    3: Book(
        id=3,
        title="The Return of the King",
        author="J.R.R. Tolkien",
        publication_year=1955,
        genre=Genre.FANTASY,
    ),
}

# --------------------------
# MISSING ENDPOINT ADDED
# --------------------------
@router.get("/books/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int):
    """Get a single book by ID with proper 404 handling"""
    book = db.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book

# --------------------------
# EXISTING ENDPOINTS IMPROVED
# --------------------------
@router.post("/books", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book: Book):
    """Create a new book entry"""
    db.add_book(book)
    return book

@router.get("/books", response_model=OrderedDict[int, Book])
async def get_books():
    """Get all books in the database"""
    return db.get_books()

@router.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, book: Book):
    """Update an existing book with error handling"""
    existing_book = db.get_book(book_id)
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return db.update_book(book_id, book)

# --------------------------
# DISABLED DELETE FUNCTIONALITY
# --------------------------
@router.delete("/books/{book_id}", status_code=status.HTTP_403_FORBIDDEN)
async def delete_book(book_id: int):
    """Delete endpoint disabled per project requirements"""
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Deleting books is not allowed"
    )

