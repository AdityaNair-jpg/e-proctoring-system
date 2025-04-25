from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import subprocess
from sqlalchemy import text
from models import db, Test
from flask import send_from_directory
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for communication with React frontend

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:hello123@localhost:3308/proctoring_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# ======= DATABASE MODEL =======
class Test(db.Model):
    __tablename__ = 'test'
    __table_args__ = {'extend_existing': True} 

    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100), nullable=False)
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



@app.route('/start_proctoring', methods=['GET'])
def start_proctoring():
    try:
        subprocess.Popen(['python', 'fd.py'])  # Replace with your actual face detection file
        return jsonify({'message': 'Proctoring started successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route("/test_db")
def test_db():
    try:
        db.session.execute(text("SELECT 1"))
        return "✅ MySQL connection successful!"
    except Exception as e:
        return f"❌ MySQL connection failed: {str(e)}"

@app.route("/show_tables")
def show_tables():
    try:
        result = db.session.execute(text("SHOW TABLES"))
        tables = [row[0] for row in result]
        return f"Connected to 'proctoring_db'. Tables: {tables}" if tables else "Connected to 'proctoring_db'. No tables found yet."
    except Exception as e:
        return f"❌ Error accessing database: {str(e)}"
    
@app.route('/save_test', methods=['POST'])
def save_test():
    data = request.json
    test_name = data.get('test_name')
    form_link = data.get('form_link')

    if not test_name or not form_link:
        return jsonify({'error': 'Missing test_name or form_link'}), 400

    try:
        new_test = Test(test_name=test_name, form_link=form_link)
        db.session.add(new_test)
        db.session.commit()
        print(f"✅ Saved: {test_name} - {form_link}")
        return jsonify({'message': 'Test saved successfully'}), 200
    except Exception as e:
        print(f"❌ Error saving test: {e}")
        return jsonify({'error': 'Failed to save test'}), 500
    
@app.route('/get_tests', methods=['GET'])
def get_tests():
    try:
        tests = Test.query.all()
        test_list = [{
            'test_name': test.test_name,
            'form_link': test.form_link,
            'created_at': test.created_at.strftime('%Y-%m-%d %H:%M:%S')
        } for test in tests]

        return jsonify(test_list), 200
    except Exception as e:
        print(f"Error fetching tests: {e}")
        return jsonify({'error': 'Failed to fetch tests'}), 500
@app.route('/save_report', methods=['POST'])
def save_report():
    data = request.json
    report_name = data.get('report_name')
    graph_name = data.get('graph_name')

    if not report_name or not graph_name:
        return jsonify({'error': 'Missing data'}), 400

    try:
        db.session.execute(text(
            "INSERT INTO history (report_name, graph_name) VALUES (:report_name, :graph_name)"
        ), {"report_name": report_name, "graph_name": graph_name})
        db.session.commit()
        return jsonify({'message': 'Report saved to history'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_reports', methods=['GET'])
def get_reports():
    try:
        result = db.session.execute(text("SELECT * FROM history ORDER BY created_at DESC"))
        reports = [{
            "id": row[0],
            "report_name": row[1],
            "graph_name": row[2],
            "created_at": row[3].strftime('%Y-%m-%d %H:%M:%S')
        } for row in result]
        return jsonify(reports), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/log_suspicious', methods=['POST'])
def log_suspicious():
    data = request.json
    event = data.get('event')
    timestamp = data.get('timestamp')

    # Just print/log it for now
    print(f"🕵️ Suspicious: {event} at {timestamp}")

    # Optional: append to session list, or save to a database or file
    # suspicious_events.append(f"{timestamp} - {event}")

    return jsonify({"message": "Suspicious activity logged"}), 200

    
@app.route('/download_report/<filename>')
def download_report(filename):
    reports_dir = os.path.join(os.getcwd(), 'reports')
    file_path = os.path.join(reports_dir, filename)

    if not os.path.exists(file_path):
        return {"error": "File not found"}, 404

    return send_from_directory(reports_dir, filename, as_attachment=True, mimetype='application/pdf')

# ======= MAIN =======
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
