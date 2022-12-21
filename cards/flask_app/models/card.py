from flask_app import app
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User

db="card_tracker_schema"

class Card:
    def __init__(self, data):
        print(data)
        self.id=data["id"]
        self.title=data["title"]
        self.graded=data["graded"]
        self.graded=data["league"]
        self.price=data["price"]
        self.date_of_print=data["date_of_print"]
        self.user_id=data["user_id"]
        self.created_at=data["created_at"]
        self.updated_at=data["updated_at"]
        self.poster_first_name=data["first_name"]
        self.poster_last_name=data["last_name"]
        self.owner=[]

    @classmethod
    def create(cls,data):
        query="INSERT INTO cards (title, graded, price, date_of_print, league, user_id) VALUES (%(title)s, %(graded)s, %(price)s, %(date_of_print)s, %(league)s, %(user_id)s)"
        return connectToMySQL(db).query_db(query,data)

    @classmethod
    def update(cls,data):
        query="UPDATE cards SET title=%(title)s, graded=%(graded)s, price=%(price)s, date_of_print=%(date_of_print)s, league=%(league)s WHERE id=%(id)s;"
        results =connectToMySQL(db).query_db(query, data)
        return results

    @classmethod
    def get_one(cls,data):
        query= "SELECT * FROM cards JOIN users ON users.id=cards.user_id WHERE cards.id = %(id)s"
        results= connectToMySQL(db).query_db(query,data)
        print(results)
        return results

    @classmethod
    def get_all(cls):
        query="SELECT * FROM cards JOIN users ON users.id=cards.user_id"
        results= connectToMySQL(db).query_db(query)
        cards=[]
        for row in results:
            cards.append(Card(row))
        return cards

    @classmethod
    def get_all_from_one(cls,data):
        query = "SELECT * FROM cards JOIN users ON users.id=cards.user_id WHERE users.id =%(id)s;"
        results = connectToMySQL(db).query_db(query,data)
        all_cards=[]
        for card in results:
            owner=cls(card)
            owner_info={
                "id":card["users.id"],
                "league":card["league"],
                "password":card["password"],
                "created_at":card["users.created_at"],
                "updated_at":card["users.updated_at"],
                "first_name":card["first_name"],
                "last_name":card["last_name"],
                "email":card["email"],
                }
            owner.owner=User(owner_info)
            all_cards.append(owner)
        return all_cards

    @classmethod
    def destroy(cls,data):
        query="DELETE FROM cards WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)


    @staticmethod
    def validate_card(card):
        is_valid=True
        if len(card['title']) <5:
            is_valid=False
            flash("Card title must be more than 5 characters.", "card")
        if len(card['price']) <2:
            is_valid=False
            flash("Price must be a valid number greater than 2.", "card")
        return is_valid
