from flask import Flask, request, jsonify, send_from_directory
import matplotlib.pyplot as plt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
import os
import datetime
import io

app = Flask(__name__)

# Ensure reports directory exists
if not os.path.exists('reports'):
    os.makedirs('reports')

@app.route('/save_report', methods=['POST'])
def save_report():
    data = request.json
    try:
        session_start = data['session_start']
        session_end = data['session_end']
        suspicion_events = data['suspicious_events']  # list of event strings
        timestamps = data['timestamps']               # list of floats
        suspicion_levels = data['suspicion_levels']   # list of ints

        # Duration
        start_dt = datetime.datetime.fromisoformat(session_start)
        end_dt = datetime.datetime.fromisoformat(session_end)
        duration = str(end_dt - start_dt)

        # Filenames
        timestamp_str = end_dt.strftime('%Y%m%d_%H%M%S')
        graph_filename = f"suspicion_graph_{timestamp_str}.png"
        pdf_filename = f"session_report_{timestamp_str}.pdf"

        # Save graph
        plt.figure()
        plt.plot(timestamps, suspicion_levels, 'r-', label='Suspicion Level')
        plt.xlabel('Time (s)')
        plt.ylabel('Suspicion Level')
        plt.title('Suspicion Level Over Time')
        plt.legend()
        graph_path = os.path.join('reports', graph_filename)
        plt.savefig(graph_path)
        plt.close()

        # Generate PDF
        pdf_path = os.path.join('reports', pdf_filename)
        c = canvas.Canvas(pdf_path, pagesize=A4)
        c.setFont("Helvetica", 12)

        c.drawString(50, 800, "E-Proctoring Session Report")
        c.drawString(50, 780, f"Session Start: {session_start}")
        c.drawString(50, 765, f"Session End: {session_end}")
        c.drawString(50, 750, f"Duration: {duration}")
        c.drawString(50, 735, f"Total Suspicious Events: {len(suspicion_events)}")

        # Draw suspicious events
        y_pos = 715
        c.setFont("Helvetica", 10)
        if suspicion_events:
            c.drawString(50, y_pos, "Suspicious Activity Log:")
            y_pos -= 15
            for event in suspicion_events:
                if y_pos < 100:
                    c.showPage()
                    y_pos = 800
                c.drawString(60, y_pos, f"- {event}")
                y_pos -= 12
        else:
            c.drawString(50, y_pos, "No suspicious activity detected.")

        # Embed graph
        c.showPage()
        c.drawString(50, 800, "Suspicion Level Over Time")
        c.drawImage(graph_path, 50, 300, width=500, height=400)

        c.save()

        return jsonify({
            "message": "✅ Report saved",
            "pdf": pdf_filename,
            "graph": graph_filename
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/get_reports', methods=['GET'])
def get_reports():
    files = os.listdir('reports')
    reports = [f for f in files if f.endswith('.pdf')]
    return jsonify({"reports": reports})

@app.route('/reports/<filename>', methods=['GET'])
def serve_report(filename):
    return send_from_directory('reports', filename)

if __name__ == '__main__':
    app.run(debug=True)
