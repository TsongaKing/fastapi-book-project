from fastapi import APIRouter, Depends, HTTPException, status
from api.db.schemas import Book, Genre, InMemoryDB
from typing import OrderedDict

router = APIRouter(prefix="/books", tags=["books"])

# --------------------------
# Dependency Injection Setup
# --------------------------
def get_database() -> InMemoryDB:
    """Dependency that provides the initialized in-memory database"""
    db = InMemoryDB()
    # Initialize with sample data
    db.books = OrderedDict({
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
    })
    return db

# --------------------------
# Endpoint Definitions
# --------------------------
@router.get("", response_model=OrderedDict[int, Book])
async def get_books(db: InMemoryDB = Depends(get_database)):
    """Get all books in the system"""
    return db.get_books()

@router.get("/{book_id}", response_model=Book)
async def get_book(
    book_id: int, 
    db: InMemoryDB = Depends(get_database)
):
    """Get a specific book by its ID"""
    book = db.get_book(book_id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book

@router.post("", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(
    book: Book,
    db: InMemoryDB = Depends(get_database)
):
    """Create a new book entry"""
    try:
        return db.add_book(book)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{book_id}", response_model=Book)
async def update_book(
    book_id: int,
    book: Book,
    db: InMemoryDB = Depends(get_database)
):
    """Update an existing book's details"""
    try:
        return db.update_book(book_id, book)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

@router.delete("/{book_id}", status_code=status.HTTP_403_FORBIDDEN)
async def delete_book(
    book_id: int,
    db: InMemoryDB = Depends(get_database)
):
    """Delete a book entry (disabled operation)"""
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Deleting books is not allowed"
    )