import React, { useState } from 'react';

const AddTest = () => {
  const [showDialog, setShowDialog] = useState(false);
  const [testName, setTestName] = useState('');
  const [formLink, setFormLink] = useState('');

  const handleSave = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/save_test', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          test_name: testName,
          form_link: formLink,
        }),
      });

      if (response.ok) {
        alert('Test saved successfully!');
        setTestName('');
        setFormLink('');
        setShowDialog(false);
      } else {
        alert('Failed to save test.');
      }
    } catch (error) {
      console.error('Error:', error);
      alert('Error saving test.');
    }
  };

  return (
    <div className="flex flex-col items-center mt-8 w-dvw">
      {/* Add Test Trigger */}
      <p
        onClick={() => setShowDialog(true)}
        className="cursor-pointer bg-blue-800 text-white px-6 py-2 rounded shadow hover:bg-blue-600 transition"
      >
        Add Test
      </p>

      {/* Dialog */}
      {showDialog && (
        <div className="mt-6 w-full max-w-md bg-gray border border-gray-300 rounded-lg shadow-md p-6">
          <h2 className="text-xl font-semibold mb-4 text-blue-800">Add New Test</h2>

          <input
            type="text"
            placeholder="Test Name"
            value={testName}
            onChange={(e) => setTestName(e.target.value)}
            className="w-full p-2 mb-3 border border-gray-300 rounded text-black font-bold"
          />

          <input
            type="text"
            placeholder="Google Form Link"
            value={formLink}
            onChange={(e) => setFormLink(e.target.value)}
            className="w-full p-2 mb-4 border border-gray-300 rounded text-black font-bold"
          />

          <div className="flex justify-end space-x-3">
            <button
              onClick={handleSave}
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
              Save
            </button>
            <button
              onClick={() => setShowDialog(false)}
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
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default AddTest;
