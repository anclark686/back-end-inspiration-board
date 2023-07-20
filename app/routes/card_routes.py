from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.card import Card
from .routes_helpers import validate_model


card_bp = Blueprint("cards", __name__, url_prefix="/cards")


@card_bp.route("", methods=["POST"])
def create_card():
    request_body = request.get_json()

    try:
        new_card = Card.from_dict(request_body)
    except KeyError:
        abort(make_response(jsonify({"details": "Invalid data"}), 400))

    db.session.add(new_card)
    db.session.commit()

    return make_response(jsonify(new_card.to_dict()), 201)


@card_bp.route("", methods=["GET"])
def get_all_cards():
    cards = Card.query.all()
    cards_response = [card.to_dict() for card in cards]

    return make_response(jsonify(cards_response), 200)


@card_bp.route("/<id>", methods=["DELETE"])
def delete_one_card(id):
    card = validate_model(Card, id)

    db.session.delete(card)
    db.session.commit()
    
    return make_response(jsonify({"details": f'Card {card.card_id} successfully deleted'}), 200)


@card_bp.route("/<id>/add_like", methods=["PATCH"])
def add_like(id):
    card = validate_model(Card, id)

    card.likes_count += 1
    db.session.commit()


    return make_response(jsonify({"card_like_count": card.likes_count}), 200)
