from database import create_db_and_tables, get_session
from schema import Book
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session
import uvicorn


SessionDep = Annotated[Session, Depends(get_session)]


async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    pass


app = FastAPI(lifespan=lifespan)


@app.get("/health/liveness", tags=["Health"])
def liveness_probe():
    return {"status": "alive"}


@app.get("/health/readiness", tags=["Health"])
def readiness_probe():
    return {"status": "ready"}


@app.post("/books/")
def create_book(book: Book, session: SessionDep) -> Book:
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


@app.get("/books/{book_id}")
def get_book(book_id: int, session: SessionDep) -> Book:
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book, session: SessionDep) -> Book:
    existing_book = session.get(Book, book_id)
    if not existing_book:
        raise HTTPException(status_code=404, detail="book not found")
    for key, value in book.model_dump().items():
        setattr(existing_book, key, value)
    session.commit()
    session.refresh(existing_book)
    return existing_book


@app.delete("/books/{book_id}")
def delete_book(book_id: int, session: SessionDep) -> Book:
    book = session.get(Book, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="book not found")
    session.delete(book)
    session.commit()
    return {"detail": "book deleted"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
