import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Movie Recommendation API"}

def test_get_movies():
    response = client.get("/movies")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_movie_by_id():
    response = client.get("/movies/1")
    assert response.status_code == 200
    assert "title" in response.json()
    assert "genre" in response.json()

def test_get_movie_not_found():
    response = client.get("/movies/9999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Movie not found"}

def test_recommend_movies():
    response = client.post("/recommend", json={"user_id": 1})
    assert response.status_code == 200
    assert isinstance(response.json(), list)