from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.board import Board
from .routes_helpers import validate_model

# example_bp = Blueprint('example_bp', __name__)
board_bp = Blueprint("boards", __name__, url_prefix="/boards")

@board_bp.route("", methods=["GET"])
def get_all_boards():
    boards = Board.query.all()
    boards_response = [board.to_dict() for board in boards]
    return make_response(jsonify(boards_response), 200)

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
