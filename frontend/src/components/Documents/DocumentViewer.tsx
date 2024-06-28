import React, { useEffect, useState } from "react";
import { Worker, Viewer } from '@react-pdf-viewer/core';
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';
import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';
import { DocumentOut } from "../../client/models/DocumentOut";

interface DocumentViewerProps {
    documentDetails: DocumentOut;
    fileBlob: Blob;
    fileType: string;
    fileName?: string;
    additionalInfo?: string;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ documentDetails, fileBlob, fileType }) => {
    const [fileUrl, setFileUrl] = useState<string>('');

    useEffect(() => {
        const url = URL.createObjectURL(fileBlob);
        setFileUrl(url);
        return () => {
            URL.revokeObjectURL(url);
        };
    }, [fileBlob]);

    const defaultLayoutPluginInstance = defaultLayoutPlugin();

    return (
        <div>
            <h3>Title: {documentDetails.title}</h3>
            {documentDetails.file && <h3>File Name: {documentDetails.file}</h3>}
            <h3>Owner: {documentDetails.owner.full_name}</h3>
            <h3>Status: {documentDetails.status}</h3>
            {fileType === "application/pdf" && fileUrl && (
                <Worker workerUrl={`https://unpkg.com/pdfjs-dist@3.4.120/build/pdf.worker.min.js`}>
                    <div style={{ height: '750px' }}>
                        <Viewer fileUrl={fileUrl} plugins={[defaultLayoutPluginInstance]} />
                    </div>
                </Worker>
            )}
        </div>
    );
};

export default DocumentViewer;
