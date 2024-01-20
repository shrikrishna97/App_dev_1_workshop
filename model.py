from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class User(db.Model):
#     user_id = db.Column(db.Integer,primary_key=True,autoincrement=True)
#     email = db.Column(db.String(200),nullable=False)
#     password = db.Column(db.String(20),nullable=False)

#     def __repr__(self):
#         return '<User (email = %s, password = %s)>' %(self.email, self.password)
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)  
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    # ebooks = db.relationship('EBook', backref='owner', lazy=True)
    sections = db.relationship('Section', backref='owner', lazy=True)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sec_name = db.Column(db.String(100), nullable=False)
    sec_description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
 