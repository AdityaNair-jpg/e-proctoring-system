import React from "react";

const StartButton = () => {
  const startProctoring = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/start_proctoring", {
        method: "GET",
      });
  
      if (!response.ok) {
        throw new Error("Failed to start proctoring");
      }
  
      const data = await response.json();
      alert(data.message); // Show success message
  
    } catch (error) {
      console.error("Error:", error);
      alert("Error starting proctoring. Check console for details.");
    }
  };

  return (
    <><h1 className="text-white">Invigilease</h1>
    <button onClick={startProctoring} className="text-red-600 placeholder-indigo-200">
      Start Proctoring
    </button></>
  );
};

export default StartButton;
