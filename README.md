# Book Inventory Microservice

This is a FastAPI-based microservice for managing an inventory of books. It connects to a SQLite backend and provides standard CRUD endpoints, along with readiness and liveness probes.

## Features

- CRUD operations for books:
  - Create a book
  - Retrieve a book by ID
  - Update a book
  - Delete a book
- Health probes:
  - Liveness: `/health/liveness`
  - Readiness: `/health/readiness`

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- SqlModel
- pytest
- pytest-cov

## Setup

1. Install dependencies:
   ```bash
   uv init
   uv venv
   source .venv/bin/activate
   uv pip install -r requirements.text
   ```


2. Run the application:
   ```bash
   python main.py
   ```

3. Access the API at `http://127.0.0.1:8000`.

4. Access the API documentation at `http://127.0.0.1:8000/docs`.

## Endpoints

- **Book Management**
  - `POST /books/` - Create a new book
  - `GET /books/{book_id}` - Retrieve a book by ID
  - `PUT /books/{book_id}` - Update a book
  - `DELETE /books/{book_id}` - Delete a book

- **Health Probes**
  - `GET /health/liveness` - Check if the service is alive
  - `GET /health/readiness` - Check if the service is ready

## License

This project is licensed under MIT License