from sqlmodel import Field, Session, SQLModel, create_engine, select


class Book(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    author: str
    isbn: int
    price: int
    pages: int
    language: str
