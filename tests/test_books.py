from fastapi.testclient import TestClient
from api.db.schemas import Book
from main import app

client = TestClient(app)

def test_get_all_books():
    response = client.get("/api/v1/books")
    assert response.status_code == 200
    books = response.json()
    assert len(books) == 3
    [Book(**book) for book in books]  # Validate schema

def test_get_existing_book():
    response = client.get("/api/v1/books/1")
    assert response.status_code == 200
    book = Book(**response.json())
    assert book.title == "The Hobbit"
    assert book.author == "J.R.R. Tolkien"

def test_get_nonexistent_book():
    response = client.get("/api/v1/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}

def test_create_book():
    new_book = {
        "id": 4,
        "title": "Harry Potter and the Sorcerer's Stone",
        "author": "J.K. Rowling",
        "publication_year": 1997,
        "genre": "Fantasy"
    }
    response = client.post("/api/v1/books", json=new_book)
    assert response.status_code == 201
    created_book = Book(**response.json())
    assert created_book.id == 4
    
    # Verify new book exists
    response = client.get("/api/v1/books")
    assert len(response.json()) == 4

def test_update_book():
    updated_data = {
        "id": 1,
        "title": "The Hobbit: Revised Edition",
        "author": "J.R.R. Tolkien",
        "publication_year": 1937,
        "genre": "Fantasy"
    }
    response = client.put("/api/v1/books/1", json=updated_data)
    assert response.status_code == 200
    updated_book = Book(**response.json())
    assert updated_book.title == "The Hobbit: Revised Edition"

def test_delete_book_forbidden():
    response = client.delete("/api/v1/books/3")
    assert response.status_code == 403
    assert "not allowed" in response.json()["detail"]
    # Verify book still exists
    assert client.get("/api/v1/books/3").status_code == 200