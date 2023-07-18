from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from .routes_helpers import validate_model

# example_bp = Blueprint('example_bp', __name__)
card_bp = Blueprint("cards", __name__, url_prefix="/cards")


@card_bp.route("/<id>", methods=["DELETE"])
def delete_one_card(id):
    card = validate_model(Card, id)

    db.session.delete(card)
    db.session.commit()
    return make_response(jsonify({"details": f'Card {card.card_id} successfully deleted'}), 200)

# ADD LIKE TO CARD
@card_bp.route("/<id>/add_like", methods=["PATCH"])
def add_like(id):
    card = validate_model(Card, id)

    card.likes_count += 1
    db.session.commit()

    return make_response(jsonify({"card_like_count": card.likes_count}), 200)
