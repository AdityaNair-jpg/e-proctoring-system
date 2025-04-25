import React, { useEffect, useState } from "react";

const StartButton = () => {
  const [proctoringStarted, setProctoringStarted] = useState(false);

  // Suspicious Activity Logger
  useEffect(() => {
    if (!proctoringStarted) return;

    const handleBlur = () => {
      logSuspicious("Window unfocused or minimized");
    };

    const handleVisibilityChange = () => {
      if (document.hidden) {
        logSuspicious("Tab switched");
      }
    };

    const logSuspicious = async (event) => {
      try {
        await fetch("http://127.0.0.1:5000/log_suspicious", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            event,
            timestamp: new Date().toISOString(),
          }),
        });
        console.log(`Logged: ${event}`);
      } catch (error) {
        console.error("Failed to log suspicious activity:", error);
      }
    };

    // Attach listeners
    window.addEventListener("blur", handleBlur);
    document.addEventListener("visibilitychange", handleVisibilityChange);

    // Cleanup on unmount
    return () => {
      window.removeEventListener("blur", handleBlur);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, [proctoringStarted]);

  // Start Proctoring Handler
  const startProctoring = async () => {
    try {
      const response = await fetch("http://127.0.0.1:5000/start_proctoring", {
        method: "GET",
      });

      if (!response.ok) {
        throw new Error("Failed to start proctoring");
      }

      const data = await response.json();
      alert(data.message);
      setProctoringStarted(true); // Trigger suspicious activity monitoring
    } catch (error) {
      console.error("Error:", error);
      alert("Error starting proctoring. Check console for details.");
    }
  };

  return (
    <button
      onClick={startProctoring}
      style={{
        padding: "10px 20px",
        fontSize: "16px",
        backgroundColor: "#1565C0",
        color: "white",
        border: "none",
        borderRadius: "5px",
        cursor: "pointer",
        
      }}
    >
      {proctoringStarted ? "Proctoring Started" : "Start Proctoring"}
    </button>
  );
};

export default StartButton;
