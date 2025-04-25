from flask import Flask, jsonify
import subprocess

app = Flask(__name__)

@app.route('/start_proctoring', methods=['GET'])
def start_proctoring():
    try:
        # Start the face detection script
        subprocess.Popen(["python", "fd.py"])  # Adjust filename if needed
        return jsonify({"message": "Proctoring started successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
