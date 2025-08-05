import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

# Import the main FastAPI app and the dependency function
from main import app, get_session
from schema import Book

# Define the connection string for an in-memory SQLite database for testing.
# This ensures that our tests don't interfere with the actual development database.
DATABASE_URL = "sqlite:///:memory:"

# Create the test database engine with connect_args for SQLite compatibility.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})


# This function will be used as a dependency override.
# It creates a new database and session for each test, ensuring test isolation.
def get_test_session():
    # Create all tables in the in-memory database.
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        try:
            # Yield the session to the test function.
            yield session
        finally:
            # After the test is complete, close the session.
            session.close()
            # Drop all tables to leave the database clean for the next test.
            SQLModel.metadata.drop_all(engine)


# Override the original get_session dependency with our new test session dependency.
# This is a core concept of testing FastAPI applications with dependencies.
app.dependency_overrides[get_session] = get_test_session

# Create a TestClient instance. This client will make requests to the FastAPI app
# during tests, but without running a live server.
client = TestClient(app)


def test_health_liveness_probe():
    """
    Tests the /health/liveness endpoint to ensure it returns a 200 OK status.
    """
    response = client.get("/health/liveness")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_health_readiness_probe():
    """
    Tests the /health/readiness endpoint to ensure it returns a 200 OK status.
    """
    response = client.get("/health/readiness")
    assert response.status_code == 200
    assert response.json() == {"status": "ready"}


def test_create_book():
    """
    Tests the successful creation of a new book via the POST /books/ endpoint.
    """
    book_data = {
        "name": "The Hitchhiker's Guide to the Galaxy",
        "author": "Douglas Adams",
        "isbn": 9780345391803,
        "price": 42,
        "pages": 224,
        "language": "English",
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    data = response.json()
    # Check that the response contains the created book's data, including the new ID.
    assert data["name"] == book_data["name"]
    assert data["author"] == book_data["author"]
    assert "id" in data
    assert data["id"] is not None


def test_get_book():
    """
    Tests retrieving a single book by its ID.
    """
    # First, create a book to ensure there's data to retrieve.
    book_data = {
        "name": "Dune",
        "author": "Frank Herbert",
        "isbn": 9780441013593,
        "price": 15,
        "pages": 412,
        "language": "English",
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    # Now, retrieve the book by its ID.
    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == book_data["name"]
    assert data["id"] == book_id


def test_get_book_not_found():
    """
    Tests that a 404 Not Found error is returned when requesting a non-existent book.
    """
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Book not found"}


def test_update_book():
    """
    Tests successfully updating an existing book's details.
    """
    # First, create a book.
    original_book_data = {
        "name": "1984",
        "author": "G. Orwell",
        "isbn": 9780451524935,
        "price": 10,
        "pages": 328,
        "language": "English",
    }
    create_response = client.post("/books/", json=original_book_data)
    book_id = create_response.json()["id"]

    # Now, update the book's author and price.
    updated_book_data = {
        "name": "1984",
        "author": "George Orwell",  # Corrected author name
        "isbn": 9780451524935,
        "price": 12,  # Updated price
        "pages": 328,
        "language": "English",
    }
    response = client.put(f"/books/{book_id}", json=updated_book_data)
    assert response.status_code == 200
    data = response.json()
    assert data["author"] == "George Orwell"
    assert data["price"] == 12
    assert (
        data["name"] == original_book_data["name"]
    )  # Ensure other fields are unchanged


def test_update_book_not_found():
    """
    Tests that a 404 Not Found error is returned when trying to update a non-existent book.
    """
    book_data = {
        "name": "Fake Book",
        "author": "N/A",
        "isbn": 123,
        "price": 1,
        "pages": 1,
        "language": "None",
    }
    response = client.put("/books/999", json=book_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "book not found"}


def test_delete_book():
    """
    Tests successfully deleting a book.
    """
    # First, create a book to delete.
    book_data = {
        "name": "To Be Deleted",
        "author": "Temp",
        "isbn": 999999,
        "price": 1,
        "pages": 1,
        "language": "Temp",
    }
    create_response = client.post("/books/", json=book_data)
    book_id = create_response.json()["id"]

    # Delete the book.
    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 200
    assert delete_response.json() == {"detail": "book deleted"}

    # Verify the book is actually gone by trying to retrieve it.
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404


def test_delete_book_not_found():
    """
    Tests that a 404 Not Found error is returned when trying to delete a non-existent book.
    """
    response = client.delete("/books/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "book not found"}
