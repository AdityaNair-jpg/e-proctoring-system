from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()

class Test(db.Model):
    __tablename__ = 'test'  # explicitly specify the table name
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(255), nullable=False)
    form_link = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class History(db.Model):
    __tablename__ = 'history'  # explicitly specify the table name
    id = db.Column(db.Integer, primary_key=True)
    report_name = db.Column(db.String(255), nullable=False)
    graph_name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)



class User(db.Model):
    __tablename__ = 'users'  # Table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # Store hashed password
