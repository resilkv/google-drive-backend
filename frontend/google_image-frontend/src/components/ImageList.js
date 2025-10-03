import React from "react";

const ImageList = ({ images }) => {
  if (!images || !images.length) return <p>No images found</p>;

  return (
  <div
    style={{
      display: "flex",
      flexWrap: "wrap",
      marginTop: "16px",
    }}
  >
    {images.map((img) => (
      <div
        key={img.id}
        style={{
          margin: "8px",
          border: "1px solid #ccc",
          padding: "8px",
          borderRadius: "4px",
          textAlign: "center",
          width: "200px", // adjust as needed
        }}
      >
        <img
          src={img.storage_path}
          alt={img.name}
          style={{ width: "150px", height: "150px", objectFit: "cover" }}
        />
        <p style={{ fontSize: "12px", marginTop: "4px", fontWeight: "bold" }}>
          {img.name}
        </p>
        <div style={{ fontSize: "12px", textAlign: "left" }}>
          <p><strong>Google Drive ID:</strong> {img.google_drive_id}</p>
          <p><strong>Size:</strong> {img.size} bytes</p>
          <p><strong>MIME Type:</strong> {img.mime_type}</p>
          <p><strong>Created At:</strong> {new Date(img.created_at).toLocaleString()}</p>
          <p>
            <strong>Storage URL:</strong>{" "}
            <a href={img.storage_path} target="_blank" rel="noopener noreferrer">
              View
            </a>
          </p>
        </div>
      </div>
    ))}
  </div>
);
};

export default ImageList;
