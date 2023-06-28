from flask import Blueprint, request, jsonify, make_response
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
    return make_response(jsonify({"details": f'Card {card.id} successfully deleted'}), 200)