import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock
from app.auth.jwt_token import check_token_valid
from app.routers import borrow_router

app.dependency_overrides = {}
app.dependency_overrides[check_token_valid] = lambda: "test@email.com"

client = TestClient(app)

def test_create_borrow_book_success(monkeypatch):
    app.dependency_overrides[check_token_valid] = lambda: "test@email.com"
    monkeypatch.setattr(borrow_router, "get_book_by_id", AsyncMock(return_value={"id": 1, "quantity": 2}))
    monkeypatch.setattr(borrow_router, "get_reader_by_id", AsyncMock(return_value={"id": 1}))
    monkeypatch.setattr(borrow_router, "get_the_number_of_reader_borrow_books", AsyncMock(return_value=1))
    monkeypatch.setattr(borrow_router, "create_borrow", AsyncMock(return_value={"id": 1, "id_book": 1, "id_reader": 1}))
    data = {"id_book": 1, "id_reader": 1}
    response = client.post("/borrow/create", json=data, headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1

def test_return_borrow_book_success(monkeypatch):
    app.dependency_overrides[check_token_valid] = lambda: "test@email.com"
    monkeypatch.setattr(borrow_router, "return_book", AsyncMock(return_value={"id": 1, "returned": True}))
    response = client.get("/borrow/return/1", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["returned"] is True

def test_get_borrows_reader_success(monkeypatch):
    app.dependency_overrides[check_token_valid] = lambda: "test@email.com"
    monkeypatch.setattr(borrow_router, "get_borrow_by_reader_id", AsyncMock(return_value=[{"id": 1, "id_book": 1}]))
    response = client.get("/borrow/1", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)
