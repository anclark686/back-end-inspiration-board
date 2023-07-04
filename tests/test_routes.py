import unittest
from unittest.mock import Mock, patch
from app.models.card import Card
import pytest

def test_add_like_existing_card(client, one_card):
    # Arrange
    likes_count = 1

    # Act
    response = client.patch("/cards/1/add_like")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 200
    assert response_body == {"card_like_count": likes_count}
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

def test_delete_one_card(client, one_card):
    response = client.delete("/cards/1")
    response_body = response.get_json()
    print(response_body)

    assert response.status_code == 200
    assert response_body == {"details": "Card 1 successfully deleted"}

def test_delete_invalid_card(client, one_card):
    response = client.delete("/cards/hellothere")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": f"hellothere is invalid"}

def test_delete_nonexisting_card(client, one_card):
    response = client.delete("/cards/59303594")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Card with id 59303594 was not found."}
