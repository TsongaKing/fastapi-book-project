from api.db.schemas import InMemoryDB

def get_db():
    db = InMemoryDB()
    # Initialize sample books
    db.books = {1: ..., 2: ..., 3: ...}
    return db