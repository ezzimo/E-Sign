import React, { useEffect, useState } from "react";
import { DocumentOut } from "../../client/models/DocumentOut";
import { Document, Page, pdfjs } from 'react-pdf';
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.entry';

pdfjs.GlobalWorkerOptions.workerSrc = pdfjsWorker;

interface DocumentViewerProps {
    documentDetails: DocumentOut;
    fileBlob: Blob;
    fileType: string;
    fileName?: string;
    additionalInfo?: string;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ documentDetails, fileBlob, fileType }) => {
    const [fileUrl, setFileUrl] = useState<string>('');
    const [numPages, setNumPages] = useState<number | null>(null);
    const [pageNumber, setPageNumber] = useState<number>(1);
    const [scale, setScale] = useState<number>(1.0);

    useEffect(() => {
        const reader = new FileReader();
        reader.readAsDataURL(fileBlob);
        reader.onloadend = () => {
            const base64String = reader.result as string;
            setFileUrl(base64String);
        };
    }, [fileBlob]);

    const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
        setNumPages(numPages);
    };

    const handlePreviousPage = () => setPageNumber(pageNumber - 1);
    const handleNextPage = () => setPageNumber(pageNumber + 1);
    const handleZoomIn = () => setScale(scale + 0.1);
    const handleZoomOut = () => setScale(scale - 0.1);

    return (
        <div>
            <h3>Title: {documentDetails.title}</h3>
            {documentDetails.file && <h3>File Name: {documentDetails.file}</h3>}
            {fileType === "application/pdf" ? (
                <div style={{ width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                    <div>
                        <button onClick={handlePreviousPage} disabled={pageNumber <= 1}>Previous</button>
                        <span>Page {pageNumber} of {numPages}</span>
                        <button onClick={handleNextPage} disabled={pageNumber >= (numPages || 1)}>Next</button>
                    </div>
                    <div>
                        <button onClick={handleZoomOut} disabled={scale <= 0.5}>Zoom Out</button>
                        <span>Zoom: {Math.round(scale * 100)}%</span>
                        <button onClick={handleZoomIn} disabled={scale >= 2.0}>Zoom In</button>
                    </div>
                    <div style={{ overflow: 'auto', width: '100%' }}>
                        <Document
                            file={fileUrl}
                            onLoadSuccess={onDocumentLoadSuccess}
                        >
                            <Page 
                                pageNumber={pageNumber} 
                                scale={scale}
                                width={window.innerWidth * scale}
                                height={window.innerHeight * scale}
                            />
                        </Document>
                    </div>
                </div>
            ) : fileType.startsWith("image/") ? (
                <img src={fileUrl} alt="Document" style={{ width: "100%", height: "auto" }} />
            ) : (
                <a href={fileUrl} download={documentDetails.file}>
                    Download Document
                </a>
            )}
        </div>
    );
};

export default DocumentViewer;
