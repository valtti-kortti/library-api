import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock
from app.auth.jwt_token import check_token_valid
from app.routers import reader_router

app.dependency_overrides = {}
app.dependency_overrides[check_token_valid] = lambda: "test@email.com"

client = TestClient(app)

def test_create_reader_success(monkeypatch):
    app.dependency_overrides[check_token_valid] = lambda: "test@email.com"
    monkeypatch.setattr(reader_router, "create_reader", AsyncMock(return_value={"id": 1, "name": "Reader", "email": "reader@email.com"}))
    data = {"name": "Reader", "email": "reader@email.com"}
    response = client.post("/reader/create", json=data, headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Reader"

def test_get_reader_success(monkeypatch):
    app.dependency_overrides[check_token_valid] = lambda: "test@email.com"
    monkeypatch.setattr(reader_router, "get_reader_by_id", AsyncMock(return_value={"id": 1, "name": "Reader"}))
    response = client.get("/reader/1", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == 1

def test_update_reader_success(monkeypatch):
    app.dependency_overrides[check_token_valid] = lambda: "test@email.com"
    monkeypatch.setattr(reader_router, "update_reader_by_id", AsyncMock(return_value={"id": 1, "name": "Reader Updated"}))
    data = {"name": "Reader Updated"}
    response = client.patch("/reader/update/1", json=data, headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Reader Updated"

def test_delete_reader_success(monkeypatch):
    app.dependency_overrides[check_token_valid] = lambda: "test@email.com"
    monkeypatch.setattr(reader_router, "delete_reader_by_id", AsyncMock(return_value=True))
    response = client.delete("/reader/delete/1", headers={"Authorization": "Bearer testtoken"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Reader deleted"
