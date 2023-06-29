from app import db
from .board import Board
from app.routes.routes_helpers import validate_model

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    message = db.Column(db.String)
    likes_count = db.Column(db.Integer)
    board = db.relationship("Board", back_populates="cards")
    board_id = db.Column(db.Integer, db.ForeignKey('board.board_id'))


    def to_dict(self):
        card_data = {
            "card_id": self.card_id,
            "message": self.message,
            "likes_count": self.likes_count
        }
        if self.board:
            card_data["board_id"] = self.board_id
        return card_data
    
    @classmethod
    def from_dict(cls, card_data):
        new_card = Card(
            message=card_data["message"],
            likes_count=card_data["likes_count"],
            board=validate_model(Board, card_data.get("board_id"))
        )
        return new_card