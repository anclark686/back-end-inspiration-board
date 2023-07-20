import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.card import Card
from app.models.board import Board


@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def one_board(app):
    new_board = Board(title = "Do Something", owner = "Alycia")
    db.session.add(new_board)
    db.session.commit()

@pytest.fixture
def one_card(app):
    new_board = Board(title = "Do Something", owner = "Alycia")
    db.session.add(new_board)
    db.session.commit()

    new_card = Card(
        message = "A New Card", likes_count = 0, board_id = 1)
    db.session.add(new_card)
    db.session.commit()

@pytest.fixture
def four_boards(app):
    board1 = Board(title="Board 1", owner="Doris")
    board2 = Board(title="Board 2", owner="Danqing")
    board3 = Board(title="Board 3", owner="Alycia")
    board4 = Board(title="Board 4", owner="Barbara")
    
    boards = [board1, board2, board3, board4]

    for board in boards:
        db.session.add(board)
        db.session.commit()

@pytest.fixture
def two_boards_with_cards(app):
    boards = [
        Board(title="Board with Card", owner="Cardboard"),
        Board(title="Board with Cards Too", owner="Inspired")
    ]

    for board in boards:
        db.session.add(board)
        db.session.commit()

    cards = [
        Card(message="Cardboard owns this", likes_count=0, board_id=1),
        Card(message="Inspired owns this", likes_count=0, board_id=2),
        Card(message="Cardboard made this", likes_count=4, board_id=1),
    ]

    for card in cards:
        db.session.add(card)
        db.session.commit()
