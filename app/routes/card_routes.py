from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.card import Card
from .routes_helpers import validate_model

# example_bp = Blueprint('example_bp', __name__)
card_bp = Blueprint("cards", __name__, url_prefix="/cards")