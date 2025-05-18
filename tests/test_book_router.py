import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock
from app.auth.jwt_token import check_token_valid
from app.routers import book_router

app.dependency_overrides = {}
app.dependency_overrides[check_token_valid] = lambda: "test@email.com"

client = TestClient(app)

def test_create_book_success(monkeypatch):
    monkeypatch.setattr(book_router, "create_book", AsyncMock(return_value={"id": 1, "title": "Book", "author": "Author", "quantity": 1, "year": 2020, "isbn": "123"}))
    data = {"title": "Book", "author": "Author", "quantity": 1, "year": 2020, "isbn": "123"}
    response = client.post("/book/create", json=data, headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Book"

def test_get_book_success(monkeypatch):
    monkeypatch.setattr(book_router, "get_book_by_id", AsyncMock(return_value={"id": 1, "title": "Book"}))
    response = client.get("/book/get/1", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1

def test_get_books_success(monkeypatch):
    monkeypatch.setattr(book_router, "get_all_books", AsyncMock(return_value=[{"id": 1, "title": "Book"}]))
    response = client.get("/book/all")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_update_book_success(monkeypatch):
    monkeypatch.setattr(book_router, "update_book_by_id", AsyncMock(return_value={"id": 1, "title": "Book Updated"}))
    data = {"title": "Book Updated"}
    response = client.patch("/book/update/1", json=data, headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["title"] == "Book Updated"

def test_delete_book_success(monkeypatch):
    monkeypatch.setattr(book_router, "delete_book_by_id", AsyncMock(return_value=True))
    response = client.delete("/book/delete/1", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Book deleted"

def test_invalid_token_returns_401():
    # dependency_overrides не подменяем, чтобы сработала реальная проверка токена
    app.dependency_overrides = {}
    client_local = TestClient(app)
    data = {"title": "Book", "author": "Author", "quantity": 1, "year": 2020, "isbn": "123"}
    response = client_local.post("/book/create", json=data, headers={"Authorization": "Bearer invalidtoken"})
    assert response.status_code == 401
    assert response.json()["detail"] in ["Invalid or expired token", "Not authenticated", "Invalid token"]
