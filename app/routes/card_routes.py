from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from .routes_helpers import validate_model


card_bp = Blueprint("cards", __name__, url_prefix="/cards")


@card_bp.route("/<card_id>", methods=["DELETE"])
def delete_one_card(card_id):
    card = validate_model(Card, card_id)

    db.session.delete(card)
    db.session.commit()
    
    return make_response(jsonify({"details": f'Card {card.card_id} successfully deleted'}), 200)


@card_bp.route("/<card_id>/add_like", methods=["PATCH"])
def add_like(card_id):
    card = validate_model(Card, card_id)

    card.likes_count += 1
    db.session.commit()


    return make_response(jsonify({"card_like_count": card.likes_count}), 200)
