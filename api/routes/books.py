from fastapi import APIRouter, Depends, HTTPException, status
from api.db.schemas import Book, Genre
from api.db.dependencies import get_db  # Changed import
from typing import OrderedDict

router = APIRouter(prefix="/books", tags=["books"])

@router.get("", response_model=OrderedDict[int, Book])
async def get_books(db: InMemoryDB = Depends(get_db)):
    return db.get_books()


# --------------------------
# Dependency Injection Setup
# --------------------------
def get_database():
    db = InMemoryDB()
    # Initialize with sample data
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
    return db

# --------------------------
# Endpoint Definitions
# --------------------------
@router.get("", response_model=OrderedDict[int, Book])
async def get_books(db: InMemoryDB = Depends(get_database)):
    """Get all books"""
    return db.get_books()

@router.get("/{book_id}", response_model=Book)
async def get_book(book_id: int, db: InMemoryDB = Depends(get_database)):
    """Get a book by ID"""
    book = db.get_book(book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.post("", status_code=201, response_model=Book)
async def create_book(book: Book, db: InMemoryDB = Depends(get_database)):
    """Create a new book"""
    db.add_book(book)
    return book

@router.put("/{book_id}", response_model=Book)
async def update_book(
    book_id: int, 
    book: Book, 
    db: InMemoryDB = Depends(get_database)
):
    """Update a book"""
    existing = db.get_book(book_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Book not found")
    return db.update_book(book_id, book)

@router.delete("/{book_id}", status_code=403)
async def delete_book(book_id: int, db: InMemoryDB = Depends(get_database)):
    """Delete endpoint (disabled)"""
    raise HTTPException(
        status_code=403,
        detail="Deleting books is not allowed"
    )