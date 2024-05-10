import React from "react";

interface DocumentViewerProps {
  fileUrl: string;
  fileType: string;
  fileName?: string; // Optional file name
  additionalInfo?: string; // Additional context if needed
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({
  fileUrl,
  fileType,
  fileName,
  additionalInfo
}) => {
  return (
    <div>
      {/* Display file information if available */}
      {fileName && <h3>File Name: {fileName}</h3>}
      {additionalInfo && <p>{additionalInfo}</p>}
      
      {/* Render the appropriate viewer based on file type */}
      {fileType === "application/pdf" ? (
        <iframe src={fileUrl} width="100%" height="600px" />
      ) : fileType.startsWith("image/") ? (
        <img src={fileUrl} alt="Document" style={{ width: "100%", height: "auto" }} />
      ) : (
        // Fallback for other file types
        <a href={fileUrl} download>
          Download Document
        </a>
      )}
    </div>
  );
};

export default DocumentViewer;
