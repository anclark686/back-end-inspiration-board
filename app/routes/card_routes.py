from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from .routes_helpers import validate_model

# example_bp = Blueprint('example_bp', __name__)
card_bp = Blueprint("cards", __name__, url_prefix="/cards")


# ADD LIKE TO CARD
@card_bp.route("/<id>/add_like", methods=["PATCH"])
def mark_incomplete(id):
    card = validate_model(Card, id)

    card.completed_at = None
    db.session.commit()

    return make_response(jsonify({"card": card.to_dict()}), 200)
