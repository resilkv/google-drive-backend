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
            padding: "4px",
            borderRadius: "4px",
            textAlign: "center",
          }}
        >
          <img
            src={img.storage_path}
            alt={img.name}
            style={{ width: "150px", height: "150px", objectFit: "cover" }}
          />
          <p style={{ fontSize: "12px", marginTop: "4px" }}>{img.name}</p>
        </div>
      ))}
    </div>
  );
};

export default ImageList;
