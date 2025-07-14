from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from ext import db, login_manager


class User(db.Model, UserMixin):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    gender = db.Column(db.String)
    birthday = db.Column(db.Date)
    country = db.Column(db.String)
    profile_image = db.Column(db.String)
    coins = db.Column(db.Integer)
    role = db.Column(db.String)
    owned_books = db.Column(db.String)

    def check_password(self, unhashed_password):
        return check_password_hash(self.password, unhashed_password)

class Book(db.Model):

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String)
    author = db.Column(db.String)
    img = db.Column(db.String)
    price = db.Column(db.Integer)
    price_in_coins = db.Column(db.Integer)
    description = db.Column(db.String)
    pdf = db.Column(db.String)
    questions = db.Column(db.String)
    answers = db.Column(db.String)
    correct_answers = db.Column(db.String)

class Quiz(db.Model):

    __tablename__ = "quiz"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.String)
    book_id = db.Column(db.String)
    q_id = db.Column(db.String)
    user_answer = db.Column(db.String)


@login_manager.user_loader
def load_user (user_id):
    return User.query.get(user_id)
