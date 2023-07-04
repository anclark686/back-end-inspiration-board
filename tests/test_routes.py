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


def test_add_like_invalid_card(client):
    # Act
    response = client.patch("/cards/something/add_like")
    response_body = response.get_json()

    # Assert
    assert response.status_code == 400
    assert response_body == {"message": f"something is invalid"}


def test_create_one_card(client, one_board):

    response = client.post("/boards/1/cards", json={
        "likes_count": 0,
        "message": "Test card",
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "board_id": 1,
        "card_id": 1,
        "likes_count": 0,
        "message": "Test card"
    }

    new_card = Card.query.get(1)
    assert new_card
    assert new_card.message == "Test card"
    assert new_card.likes_count == 0


# def test_post_task_ids_to_goal(client, one_goal, three_tasks):
#     # Act
#     response = client.post("/goals/1/tasks", json={
#         "task_ids": [1, 2, 3]
#     })
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert "id" in response_body
#     assert "task_ids" in response_body
#     assert response_body == {
#         "id": 1,
#         "task_ids": [1, 2, 3]
#     }

#     # Check that Goal was updated in the db
#     assert len(Goal.query.get(1).tasks) == 3
