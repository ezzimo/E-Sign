import React from "react";

interface DocumentViewerProps {
    fileUrl: string;
    fileType: string;
    fileName?: string;
    additionalInfo?: string;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ fileUrl, fileType, fileName, additionalInfo }) => {
    const decodedFileUrl = decodeURIComponent(fileUrl);

    return (
        <div>
            {fileName && <h3>File Name: {fileName}</h3>}
            {additionalInfo && <p>{additionalInfo}</p>}

            {fileType === "application/pdf" ? (
                <iframe src={decodedFileUrl} width="100%" height="600px" />
            ) : fileType.startsWith("image/") ? (
                <img src={decodedFileUrl} alt="Document" style={{ width: "100%", height: "auto" }} />
            ) : (
                <a href={decodedFileUrl} download>
                    Download Document
                </a>
            )}
        </div>
    );
};

export default DocumentViewer;
