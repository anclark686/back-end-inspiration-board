from app import create_app, db
from app.models.board import Board
from app.models.card import Card

my_app = create_app()

with my_app.app_context():
    db.session.add(Card(message = "A New Card", likes_count = 0, board_id = 1)) 
    db.session.add(Card(message = "A Newer Card", likes_count = 1, board_id = 1)) 
    db.session.add(Card(message = "A Cool Card", likes_count = 0, board_id = 2)) 
    db.session.add(Card(message = "A Cooler Card", likes_count = 2, board_id = 2)) 
    db.session.add(Card(message = "A Neat Card", likes_count = 0, board_id = 3)) 
    db.session.add(Card(message = "An Awesome Card", likes_count = 3, board_id = 3)) 
    db.session.add(Card(message = "An Uncreative Card", likes_count = 0, board_id = 4)) 
    db.session.add(Card(message = "An Old Card", likes_count = 4, board_id = 4)) 

    db.session.add(Board(title = "Do Something", owner = "Alycia")) 
    db.session.add(Board(title = "Do Something Else", owner = "Alycia")) 
    db.session.add(Board(title = "Do Something More", owner = "Alycia")) 
    db.session.add(Board(title = "Do Something New", owner = "Alycia")) 

    db.session.add(Board(title = "Say Something", owner = "Barbara")) 
    db.session.add(Board(title = "Say Something Else", owner = "Barbara")) 
    db.session.add(Board(title = "Say Something More", owner = "Barbara")) 
    db.session.add(Board(title = "Say Something New", owner = "Barbara")) 

    db.session.add(Board(title = "Be Something", owner = "Danqing")) 
    db.session.add(Board(title = "Be Something Else", owner = "Danqing")) 
    db.session.add(Board(title = "Be Something More", owner = "Danqing")) 
    db.session.add(Board(title = "Be Something New", owner = "Danqing")) 

    db.session.add(Board(title = "Want Something", owner = "Doris")) 
    db.session.add(Board(title = "Want Something Else", owner = "Doris")) 
    db.session.add(Board(title = "Want Something More", owner = "Doris")) 
    db.session.add(Board(title = "Want Something New", owner = "Doris")) 
    
    db.session.commit()