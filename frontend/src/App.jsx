import React, { useState } from 'react';
import './styles/tailwind.css';

function App() {
  const [count, setCount] = useState(0);
  const [files, setFiles] = useState([]);
  const [jobDescription, setJobDescription] = useState('');

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
  };

  const handleJobDescriptionChange = (e) => {
    setJobDescription(e.target.value);
  };

  const handleFileUpload = async () => {
  if (files.length === 0) {
    alert("Please select files to upload.");
    return;
  }

  // Create FormData for sending multiple files
  const formData = new FormData();
  files.forEach(file => {
    formData.append("files[]", file);
  });

  // Add job description to the form data
  formData.append("job_desc", jobDescription);

  // Make the API call to the backend to upload the files
  try {
    const response = await fetch('http://localhost:5000/upload', {
      method: 'POST',
      body: formData,
    });

    if (response.ok) {
      const data = await response.json();
      alert("Files uploaded successfully!");
      console.log(data); // Handle the response from the server
    } else {
      alert("Failed to upload files.");
    }
  } catch (error) {
    console.error("Error uploading files:", error);
    alert("An error occurred while uploading the files.");
  }
};


  return (
    <div className="flex justify-center items-center min-h-screen bg-gradient-to-r from-blue-400 via-purple-500 to-pink-500">
      <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-lg">
        <h1 className="text-3xl font-extrabold text-center text-gray-800 mb-6">Vite + React + TailwindCSS</h1>
        
        <p className="text-lg text-gray-600 text-center mb-4">Current count: {count}</p>
        <div className="flex justify-center mb-4">
          <button
            onClick={() => setCount(count + 1)}
            className="px-8 py-3 bg-blue-600 text-white text-lg rounded-lg shadow-lg hover:bg-blue-700 transition duration-300"
          >
            Increment
          </button>
        </div>

        <div className="mb-6">
          <h2 className="text-xl font-semibold text-center mb-2">Upload Resume</h2>
          <input
            type="file"
            multiple
            onChange={handleFileChange}
            className="block w-full p-3 text-gray-700 border-2 border-gray-300 rounded-md"
          />
        </div>

        <div className="mb-6">
          <h2 className="text-xl font-semibold text-center mb-2">Job Description</h2>
          <textarea
            value={jobDescription}
            onChange={handleJobDescriptionChange}
            placeholder="Enter job description here..."
            className="w-full p-3 text-gray-700 border-2 border-gray-300 rounded-md"
            rows="6"
          />
        </div>

        <div className="flex justify-center">
          <button
            onClick={handleFileUpload}
            className="px-8 py-3 bg-green-600 text-white text-lg rounded-lg shadow-lg hover:bg-green-700 transition duration-300"
          >
            Upload Resumes
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
