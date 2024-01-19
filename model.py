from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    email = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(20),nullable=False)

    def __repr__(self):
        return '<User (email = %s, password = %s)>' %(self.email, self.password)