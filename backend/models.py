from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(255), nullable=False)
    form_link = db.Column(db.String(255), nullable=False)
