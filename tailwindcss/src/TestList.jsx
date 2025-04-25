import React, { useEffect, useState } from 'react';
import axios from 'axios';

const TestList = () => {
  const [tests, setTests] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/get_tests')
      .then((response) => {
        setTests(response.data);
      })
      .catch((error) => {
        console.error('Error fetching test data:', error);
      });
  }, []);

  return (
    <div className="p-4">
      <h2 className="text-xl font-bold mb-4  border-black text-blue-900">Test List</h2>
      {tests.length > 0 ? (
        <table className="min-w-full bg-white border-2 border-gray-400 text-blue-900">
          <thead>
            <tr>
              <th className="border px-4 py-2 border-black text-blue-900">Test Name</th>
              <th className="border px-4 py-2 border-black text-blue-900">Form Link</th>
              <th className="border px-4 py-2 border-black text-blue-900">Created At</th>
            </tr>
          </thead>
          <tbody>
            {tests.map((test, index) => (
              <tr key={index}>
                <td className="border px-4 py-2">{test.test_name}</td>
                <td className="border px-4 py-2">
                  <a href={test.form_link.startsWith('http') ? test.form_link : `https://${test.form_link}`} target="_blank" rel="noopener noreferrer" className="text-blue-500 underline">
                    {test.form_link}
                  </a>
                </td>
                <td className="border px-4 py-2">{test.created_at}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p className='text-blue-800 font-bold'>No tests found.</p>
      )}
    </div>
  );
};

export default TestList;
