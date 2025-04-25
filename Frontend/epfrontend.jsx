import { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from "recharts";

export default function EProctoringDashboard() {
  const [suspicionData, setSuspicionData] = useState([]);
  const [alertMessage, setAlertMessage] = useState("");
  const [videoUrl, setVideoUrl] = useState("http://localhost:5000/video_feed");

  useEffect(() => {
    const eventSource = new EventSource("http://localhost:5000/suspicion_stream");
    eventSource.onmessage = (event) => {
      const newData = JSON.parse(event.data);
      setSuspicionData((prev) => [...prev, newData]);
      if (newData.suspicion_level > 70) {
        setAlertMessage("⚠️ Suspicious Activity Detected!");
      } else {
        setAlertMessage("");
      }
    };
    return () => eventSource.close();
  }, []);

  return (
    <div className="p-6 flex flex-col items-center">
      <h1 className="text-3xl font-bold mb-4">E-Proctoring Dashboard</h1>
      {alertMessage && <p className="text-red-500 font-semibold text-lg">{alertMessage}</p>}
      
      <div className="flex gap-4 mt-4">
        {/* Live Video Feed */}
        <div>
          <h2 className="text-xl font-semibold">Live Feed</h2>
          <img src={videoUrl} alt="Live Proctoring Feed" className="w-96 h-64 border rounded" />
        </div>
        
        {/* Suspicion Level Graph */}
        <div>
          <h2 className="text-xl font-semibold">Suspicion Level Over Time</h2>
          <LineChart width={500} height={300} data={suspicionData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="time" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Line type="monotone" dataKey="suspicion_level" stroke="#ff0000" strokeWidth={2} />
          </LineChart>
        </div>
      </div>
      
      {/* Report Download Button */}
      <button 
        onClick={() => window.open("http://localhost:5000/download_report", "_blank")}
        className="mt-6 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
      >
        Download Report
      </button>
    </div>
  );
}
