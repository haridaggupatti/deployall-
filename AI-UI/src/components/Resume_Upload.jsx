import "./resume_upload.css"
import React, { useState } from 'react';

export default function ResumeUpload() {
  const [file, setFile] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (file) {
      const formData = new FormData();
      formData.append('file', file);  // Ensure this key matches the parameter name in FastAPI

      try {
        const response = await fetch('http://127.0.0.1:8000/upload_resume', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const resp = await response.json();
        console.log(resp);
      } catch (error) {
        console.error('Error uploading file', error);
      }
    } else {
      console.log("No file selected."); // Debug: Check if file is selected
    }
  };

  return (
    <div className="background">
        <div className="container">
        <h1>Resume Upload</h1>
        <form onSubmit={handleSubmit}>
            <input type="file" onChange={handleFileChange} />
            <button type="submit">Upload</button>
        </form>
        </div>
    </div>
  );
}
