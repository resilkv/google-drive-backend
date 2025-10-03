import React, { useState } from "react";
import { toast, ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css"; // make sure to import the CSS

const FolderInput = ({ onSubmit }) => {
  const [folderUrl, setFolderUrl] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (folderUrl) {
      onSubmit(folderUrl);

      toast.info("Images will be uploaded, please wait...", {
        position: "top-right",
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });

      setFolderUrl("");
    }
  };

  return (
    <>
      <form onSubmit={handleSubmit} style={{ marginBottom: "20px" }}>
        <input
          type="text"
          placeholder="Paste folder URL"
          value={folderUrl}
          onChange={(e) => setFolderUrl(e.target.value)}
          style={{
            width: "400px",
            padding: "8px",
            marginRight: "8px",
            border: "1px solid #ccc",
            borderRadius: "4px",
          }}
        />
        <button
          type="submit"
          style={{
            padding: "8px 16px",
            border: "none",
            backgroundColor: "#4CAF50",
            color: "#fff",
            borderRadius: "4px",
            cursor: "pointer",
          }}
        >
          Submit
        </button>
      </form>

      {/* ToastContainer must be rendered somewhere in your app */}
      <ToastContainer />
    </>
  );
};

export default FolderInput;
