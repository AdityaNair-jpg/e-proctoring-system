import React, { useEffect } from 'react';
import { Routes, Route, Link } from "react-router-dom";
import App from './epfrontend.jsx';
import AddTest from './addtest.jsx';
import TestList from './TestList.jsx';
import HistoryTab from './HistoryTab';
import AOS from 'aos';
import 'aos/dist/aos.css';

const styles = `
  html {
    scroll-behavior: smooth;
  }
  .ellipse-hover {
    position: relative;
    padding-bottom: 2px;
  }
  .ellipse-hover::after {
    content: '';
    position: absolute;
    width: 100%;
    height: 2px;
    background: currentColor;
    bottom: 0;
    left: 0;
    transform: scaleX(0);
    transform-origin: center;
    transition: transform 0.3s ease-in-out;
    border-radius: 4px;
  }
  .ellipse-hover:hover::after {
    transform: scaleX(1);
  }
  .jello-horizontal:hover {
    -webkit-animation: jello-horizontal 0.9s both;
    animation: jello-horizontal 0.9s both;
  }
  @keyframes jello-horizontal {
    0% { transform: scale3d(1, 1, 1); }
    30% { transform: scale3d(1.25, 0.75, 1); }
    40% { transform: scale3d(0.75, 1.25, 1); }
    50% { transform: scale3d(1.15, 0.85, 1); }
    65% { transform: scale3d(0.95, 1.05, 1); }
    75% { transform: scale3d(1.05, 0.95, 1); }
    100% { transform: scale3d(1, 1, 1); }
  }
  .slide-in-bck-center {
    animation: slide-in-bck-center 0.7s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
  }
  @keyframes slide-in-bck-center {
    0% {
      transform: translateZ(600px);
      opacity: 0;
    }
    100% {
      transform: translateZ(0);
      opacity: 1;
    }
  }
`;

const TopMenu = () => {
  useEffect(() => {
    AOS.init({ duration: 800, once: false });
    setTimeout(() => AOS.refresh(), 100);
  }, []);

  const infoSections = [
    {
      title: "1. Adequate Distance",
      desc: "Make sure that there is adequate distance between the user and the screen.",
    },
    {
      title: "2. Start Proctoring",
      desc: "Press the button when ready and start your test.",
    },
    {
      title: "3. Press 'Q' to Quit",
      desc: "Press Q to end the exam session and send the report to your processor.",
    },
    {
      title: "4. Face Detection",
      desc: "Ensure your face is visible throughout the session to maintain transparency.",
    },
    {
      title: "5. Eye Tracking",
      desc: "Your eyes should be focused on the screen. Look-aways may be flagged.",
    },
    {
      title: "6. Suspicious Movements",
      desc: "Movements like looking around or another face detected will raise alerts.",
    },
    {
      title: "7. Stable Internet",
      desc: "Maintain a good internet connection to avoid interruptions.",
    },
    {
      title: "8. Lighting",
      desc: "Sit in a well-lit room to ensure the webcam can see your face clearly.",
    },
    {
      title: "9. Microphone Access",
      desc: "Allow mic access so suspicious sounds can be monitored during the test.",
    },
  ];

  return (
    <>
      <style>{styles}</style>

      {/* Navbar */}
      <nav className="fixed top-0 w-full bg-white shadow-md z-50">
        <div className="container mx-auto flex justify-between items-center py-4 px-6">
          <h1 className="text-2xl font-bold text-gray-800">Invigilease</h1>
          <div className="flex space-x-8 text-lg text-gray-600 font-medium">
          <Link to="/dashboard/history" className="ellipse-hover cursor-pointer jello-horizontal">
  <p className="text-blue-800 hover:text-gray-900">History</p>
</Link>
<Link to="/dashboard/add-test" className="ellipse-hover cursor-pointer jello-horizontal">
  <p className="text-blue-800 hover:text-gray-900">Add Test</p>
</Link>
<Link to="/logout" className="ellipse-hover cursor-pointer jello-horizontal hover:text-red-600">
  <p className="text-blue-800 hover:text-red-600">Logout</p>
</Link>

          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="pt-24 pb-10 bg-gray-50 min-h-screen">
        <div className="container mx-auto px-6">
          <Routes>
            <Route
              path="/"
              element={
                <>
                  {/* Hero Section */}
                  <div className="text-center mb-10">
                    <h1 className="text-4xl font-bold slide-in-bck-center text-blue-900 mb-3">E-Proctoring Dashboard</h1>
                    <p className="text-lg text-gray-700">Your test starts here. Be prepared and follow the guidelines.</p>
                  </div>
                  <div style={{
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      height: '10vh',
      
    }}>
       <App />
    </div>
                 

                  {/* Test List */}
                  <div className="mb-12">
                    <TestList />
                  </div>

                  {/* Info Cards Section */}
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 mb-20">
                    {infoSections.map((item, index) => (
                      <div
                        key={index}
                        data-aos="fade-up"
                        data-aos-delay={index * 100}
                        className="bg-white rounded-2xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300"
                      >
                        <h2 className="text-lg font-bold text-blue-800 mb-2">{item.title}</h2>
                        <p className="text-gray-700">{item.desc}</p>
                      </div>
                    ))}
                  </div>

                  {/* Scroll Anchor */}
                  <div id="end-section" className="text-center mt-10">
                    <p className="text-sm text-gray-500">End of information. Scroll up to review guidelines.</p>
                  </div>
                </>
              }
            />
            <Route path="/add-test" element={<AddTest />} />
            <Route path="/history" element={<HistoryTab />} />
          </Routes>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-800 text-white text-center py-4">
        <p>&copy; 2025 Invigilease | All Rights Reserved</p>
      </footer>
    </>
  );
};

export default TopMenu;
