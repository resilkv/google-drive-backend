import React, { useState, useEffect } from "react";
import FolderInput from "./components/FolderInput";
import ImageList from "./components/ImageList";

const apiBase = process.env.REACT_APP_API_BASE; 
const metaBase = process.env.REACT_APP_META_BASE; 

function App() {
  const [images, setImages] = useState([]);

  // Fetch images from API
  const fetchImages = async () => {
    try {
      const res = await fetch(`${metaBase}/api/image-listing/`);
      const data = await res.json();
      setImages(data.data || []);
      
    } catch (err) {
      console.error("Failed to fetch images:", err);
    }
  };

  // Initial fetch
  useEffect(() => {
    fetchImages();
  }, []);

  // Handle folder submission
  const handleFolderSubmit = async (folderUrl) => {
    try {
      const res = await fetch(`${apiBase}/api/image-processing/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ folder_url: folderUrl }),
      });
      const data = await res.json();
      // After import, refresh the images
      fetchImages();
    } catch (err) {
      console.error("Failed to submit folder URL:", err);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}>
      <h1>Imported Images</h1>
      <FolderInput onSubmit={handleFolderSubmit} />
      <ImageList images={images} />
    </div>
  );
}

export default App;
