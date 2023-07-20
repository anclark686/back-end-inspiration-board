from unittest.mock import Mock, patch
from app.models.card import Card
from app.models.board import Board


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


def test_get_all_boards(client, four_boards):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 4
    assert response_body == [
        {
            "board_id": 1,
            "owner": "Doris",
            "title": "Board 1"
        },
        {
            "board_id": 2,
            "owner": "Danqing",
            "title": "Board 2"
        },
        {
            "board_id": 3,
            "owner": "Alycia",
            "title": "Board 3"
        },
        {
            "board_id": 4,
            "owner": "Barbara",
            "title": "Board 4"
        }
    ]

def test_delete_one_board(client, one_board):
    response = client.delete("/boards/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {"details": "Board 1 successfully deleted"}


def test_delete_invalid_board(client, one_board):
    response = client.delete("/boards/hellothere")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": f"hellothere is invalid"}


def test_delete_nonexisting_board(client, one_board):
    response = client.delete("/boards/59303594")
    response_body = response.get_json()

    assert response.status_code == 404
    assert response_body == {"message": "Board with id 59303594 was not found."}


def test_get_boards_with_cards(client, two_boards_with_cards):
    response = client.get("/boards")
    response_body = response.get_json()

    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body == [
        {
            "board_id": 1,
            "card_count": 2,
            "owner": "Cardboard",
            "title": "Board with Card"
        },
        {
            "board_id": 2,
            "card_count": 1,
            "owner": "Inspired",
            "title": "Board with Cards Too"
        },
    ]


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


def test_delete_one_card(client, one_card):
    response = client.delete("/cards/1")
    response_body = response.get_json()

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


def test_add_like_existing_card(client, one_card):
    likes_count = 1

    response = client.patch("/cards/1/add_like")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {"card_like_count": likes_count}
    assert Card.query.get(1).likes_count == likes_count


def test_add_like_missing_card(client):
    response = client.patch("/cards/1/add_like")
    response_body = response.get_json()

    assert response.status_code == 404

    assert response_body == {
        "message": "Card with id 1 was not found."
    }


def test_add_like_invalid_card(client):
    response = client.patch("/cards/something/add_like")
    response_body = response.get_json()

    assert response.status_code == 400
    assert response_body == {"message": f"something is invalid"}