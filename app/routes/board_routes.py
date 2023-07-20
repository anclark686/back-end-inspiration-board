from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from app.models.card import Card
from .routes_helpers import validate_model


board_bp = Blueprint("boards", __name__, url_prefix="/boards")


@board_bp.route("", methods=["POST"])
def create_board():
    request_body = request.get_json()
    try:
        new_board = Board.from_dict(request_body)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    db.session.add(new_board)
    db.session.commit()

    return make_response(jsonify(new_board.to_dict()), 201)


@board_bp.route("/<board_id>", methods=["GET"])
def read_one_board(board_id):
    board = validate_model(Board, board_id)

    return make_response(jsonify({"board": board.to_dict()}), 200)


@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]

    return make_response(jsonify(boards_response), 200)


@board_bp.route("/<board_id>", methods=["DELETE"])
def delete_one_board(board_id):
    board = validate_model(Board, board_id)
    
    db.session.delete(board)
    db.session.commit()

    return make_response(jsonify({"details": f'Board {board.board_id} successfully deleted'}), 200)


@board_bp.route("/<board_id>/cards", methods=["POST"])
def create_card(board_id):
    request_body = request.get_json()
    request_body["board_id"] = board_id

    try:
        new_card = Card.from_dict(request_body)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))
    
    if len(new_card.message) > 40:
        abort(make_response(jsonify({
            "details": "Message should be 40 characters or less."
            }), 400))

    db.session.add(new_card)
    db.session.commit()

    return make_response(jsonify(new_card.to_dict()), 201)


@board_bp.route("/<board_id>/cards", methods=["GET"])
def get_board_cards(board_id):
    board = validate_model(Board, board_id)
    # just a list of cards, not all the board data
    card_response = [card.to_dict() for card in board.cards]
    
    return make_response(jsonify(card_response))
