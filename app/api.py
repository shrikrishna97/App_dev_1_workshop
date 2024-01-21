from flask import Flask, request
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db1.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
api = Api(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    sections = db.relationship('Section', backref='owner', lazy=True)

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sec_name = db.Column(db.String(100), nullable=False)
    sec_description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class UserResource(Resource):
    def post(self):
        data = request.get_json()

        # Validate role
        valid_roles = ['admin', 'librarian', 'student']
        if data['role'] not in valid_roles:
            return {'error': 'Invalid role'}, 400

        # Hash password
        hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

        new_user = User(
            username=data['username'],
            email=data['email'],
            password=hashed_password,
            role=data['role']
        )

        db.session.add(new_user)
        db.session.commit()
        return {'message': 'User created successfully'}, 201

class LoginResource(Resource):
    def post(self):
        data = request.get_json()

        user = User.query.filter_by(email=data['email']).first()

        if user and bcrypt.check_password_hash(user.password, data['password']):
            return {'message': 'Login successful', 'user_id': user.id, 'role': user.role}
        else:
            return {'error': 'Invalid credentials'}, 401

class SectionResource(Resource):
    def get(self, sec_id):
        section = Section.query.get_or_404(sec_id)
        return {
            'id': section.id,
            'sec_name': section.sec_name,
            'sec_description': section.sec_description,
            'date_created': section.date_created.strftime('%Y-%m-%d %H:%M:%S'),
            'user_id': section.user_id
        }

    def put(self, sec_id):
        section = Section.query.get_or_404(sec_id)
        data = request.get_json()

        section.sec_name = data['sec_name']
        section.sec_description = data['sec_description']

        db.session.commit()
        return {'message': 'Section updated successfully'}

    def delete(self, sec_id):
        section = Section.query.get_or_404(sec_id)
        db.session.delete(section)
        db.session.commit()
        return {'message': 'Section deleted successfully'}

class SectionListResource(Resource):
    def get(self):
        sections = Section.query.all()
        result = []
        for section in sections:
            result.append({
                'id': section.id,
                'sec_name': section.sec_name,
                'sec_description': section.sec_description,
                'date_created': section.date_created.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id': section.user_id
            })
        return result

    def post(self):
        data = request.get_json()

        new_section = Section(
            sec_name=data['sec_name'],
            sec_description=data['sec_description'],
            user_id=data['user_id']
        )

        db.session.add(new_section)
        db.session.commit()
        return {'message': 'Section created successfully'}, 201

api.add_resource(UserResource, '/api/users')
api.add_resource(LoginResource, '/api/login')
api.add_resource(SectionListResource, '/api/sections')
api.add_resource(SectionResource, '/api/sections/<int:sec_id>')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
