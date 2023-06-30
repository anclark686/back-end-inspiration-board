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
def one_card(app, one_board):
    new_board = Board(title = "Do Something", owner = "Alycia")
    db.session.add(new_board)
    db.session.commit()

    new_card = Card(
        message = "A New Card", likes_count = 0, board_id = 1)
    db.session.add(new_card)
    db.session.commit()
