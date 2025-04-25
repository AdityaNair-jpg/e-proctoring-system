import React, { useEffect, useState } from 'react';
import axios from 'axios';

const HistoryTab = () => {
  const [reports, setReports] = useState([]);

  useEffect(() => {
    axios.get("http://localhost:5000/get_reports")
      .then(res => setReports(res.data))
      .catch(err => console.error(err));
  }, []);

  const handleDownload = async (reportName) => {
    try {
      const res = await fetch(`http://localhost:5000/download_report/${reportName}`);
      const blob = await res.blob();

      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = reportName; // Ensure the file is saved as .pdf
      link.click();
    } catch (err) {
      console.error("Download error:", err);
    }
  };

  return (
    <div className="w-dvw">
      <h2 className="text-xl font-bold mb-4 text-blue-900">Proctoring History</h2>
      <table className="table-auto w-6xl border-collapse border border-gray-700">
        <thead className="bg-blue-900">
          <tr>
            <th className="border p-2">Report</th>
            <th className="border p-2">Date & Time</th>
            <th className="border p-2">Action</th>
          </tr>
        </thead>
        <tbody>
          {reports.map((r, idx) => (
            <tr key={idx}>
              <td className="border p-2 font-bold text-blue-800">{r.report_name}</td>
              <td className="border p-2 font-bold text-blue-800">{r.created_at}</td>
              <td className="border p-2 font-bold text-blue-800">
                <button
                  style={{
                    padding: "10px 20px ",
                    fontSize: "16px",
                    backgroundColor: "#1565C0",
                    color: "white",
                    border: "none",
                    borderRadius: "5px",
                    cursor: "pointer",
                    
                  }}
                  onClick={() => handleDownload(r.report_name)}
                >
                  Download PDF
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default HistoryTab;
