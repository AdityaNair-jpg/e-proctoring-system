from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import subprocess

app = Flask(__name__)
CORS(app)  # Enable CORS for communication with React frontend

# ======= CONFIGURE DATABASE =======
# For SQLite (simple setup, no installation needed)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tests.db'

# Uncomment below if using MySQL instead
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/eproctoring'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======= DATABASE MODEL =======
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    form_link = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ======= INITIALIZE DB =======
with app.app_context():
    db.create_all()

# ======= ROUTES =======
@app.route('/add_test', methods=['POST'])
def add_test():
    data = request.get_json()
    name = data.get('name')
    link = data.get('form_link')

    if not name or not link:
        return jsonify({'error': 'Missing name or link'}), 400

    new_test = Test(name=name, form_link=link)
    db.session.add(new_test)
    db.session.commit()

    return jsonify({'message': 'Test added successfully'}), 200

@app.route('/get_tests', methods=['GET'])
def get_tests():
    tests = Test.query.all()
    return jsonify([
        {
            'id': t.id,
            'name': t.name,
            'form_link': t.form_link,
            'created_at': t.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for t in tests
    ])

@app.route('/start_proctoring', methods=['GET'])
def start_proctoring():
    try:
        subprocess.Popen(['python', 'main_proctor.py'])  # Replace with your actual face detection file
        return jsonify({'message': 'Proctoring started successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ======= MAIN =======
if __name__ == '__main__':
    app.run(debug=True)