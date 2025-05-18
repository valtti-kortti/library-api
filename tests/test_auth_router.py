import pytest
from fastapi import status
from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock
from app.routers import auth_router

app.dependency_overrides = {}

client = TestClient(app)

def test_register_librarian_success(monkeypatch):
    monkeypatch.setattr(auth_router, "register_librarian", AsyncMock(return_value="testtoken"))
    data = {"email": "test@example.com", "password": "1234"}
    response = client.post("/auth/register", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] == "testtoken"

def test_register_librarian_fail(monkeypatch):
    monkeypatch.setattr(auth_router, "register_librarian", AsyncMock(return_value=None))
    data = {"email": "test@example.com", "password": "1234"}
    response = client.post("/auth/register", json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_login_librarian_success(monkeypatch):
    monkeypatch.setattr(auth_router, "login_librarian", AsyncMock(return_value="testtoken"))
    data = {"email": "test@example.com", "password": "1234"}
    response = client.post("/auth/login", json=data)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["access_token"] == "testtoken"

def test_login_librarian_fail(monkeypatch):
    monkeypatch.setattr(auth_router, "login_librarian", AsyncMock(return_value=None))
    data = {"email": "test@example.com", "password": "1234"}
    response = client.post("/auth/login", json=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
