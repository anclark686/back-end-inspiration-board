import unittest
from unittest.mock import Mock, patch
from app.models.card import Card
import pytest

from app.models.board import Board
import pytest


def test_create_board(client):
    response = client.post("/boards", json={
        "title": "New Board",
        "owner": "John Doe"
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert "board_id" in response_body
    assert response_body["title"] == "New Board"
    assert response_body["owner"] == "John Doe"

def test_create_board_missing_data(client):
    response = client.post("/boards", json={
        "title": "New Board"
    })
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {
        "details": "Invalid data"
    }

def test_add_like_existing_card(client, one_card):
    # Arrange
    likes_count = 1

    # Act
    response = client.patch("/cards/1/add_like")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {"card like count": likes_count}
    assert Card.query.get(1).likes_count == likes_count

def test_add_like_missing_card(client):
    # Act
    response = client.patch("/cards/1/add_like")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 404

    # raise Exception("Complete test with assertion about response body")
    assert response_body == {
        "message": "Card with id 1 was not found."
    }


def test_get_board(client, one_board):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert "board" in response_body
    assert response_body == {'board': 
                             {'board_id': 1, 'owner': 'Alycia', 'title': 'Do Something'}
                             }

def test_get_board_not_found(client):
    response = client.get("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {'message': 'Board with id 1 was not found.'}