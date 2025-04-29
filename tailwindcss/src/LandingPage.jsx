// LandingPage.jsx
import React from 'react';
import { useNavigate } from 'react-router-dom';

function LandingPage() {
    const navigate = useNavigate();

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-r from-blue-400 to-indigo-600 text-white px-4 w-dvw">
            <h1 className="text-4xl font-extrabold mb-4 tracking-wide">INVIGILEASE</h1>
            <h2 className="text-2xl font-semibold mb-8 text-center">Welcome to the E-Proctoring System</h2>
            <div className="space-x-4">
                <button
                    onClick={() => navigate('/login')}
                    className="bg-white text-blue-600 font-semibold px-6 py-2 rounded-lg hover:bg-blue-100 transition duration-300"
                >
                    Login
                </button>
                <button
                    onClick={() => navigate('/register')}
                    className="bg-white text-blue-600 font-semibold px-6 py-2 rounded-lg hover:bg-blue-100 transition duration-300"
                >
                    Register
                </button>
            </div>
        </div>
    );
}

export default LandingPage;
