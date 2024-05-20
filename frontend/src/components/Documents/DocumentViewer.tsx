import React, { useEffect, useState } from "react";
import { DocumentRead } from "../../client/models/DocumentRead";
import { Document, Page, pdfjs } from 'react-pdf';
import pdfjsWorker from 'pdfjs-dist/build/pdf.worker.entry';

pdfjs.GlobalWorkerOptions.workerSrc = pdfjsWorker;

interface DocumentViewerProps {
    documentDetails: DocumentRead;
    fileBlob: Blob;
    fileType: string;
    fileName?: string;
    additionalInfo?: string;
}

const DocumentViewer: React.FC<DocumentViewerProps> = ({ documentDetails, fileBlob, fileType }) => {
    const [fileUrl, setFileUrl] = useState<string>('');

    useEffect(() => {
        const reader = new FileReader();
        reader.readAsDataURL(fileBlob);
        reader.onloadend = () => {
            const base64String = (reader.result as string);
            setFileUrl(base64String);
        };
    }, [fileBlob]);

    const onDocumentLoadSuccess = ({ numPages }: { numPages: number }) => {
        setNumPages(numPages);
    };

    const [numPages, setNumPages] = useState<number | null>(null);
    const [pageNumber, setPageNumber] = useState<number>(1);

    return (
        <div>
            <h3>Title: {documentDetails.title}</h3>
            {documentDetails.file && <h3>File Name: {documentDetails.file}</h3>}
            {fileType === "application/pdf" ? (
                <div>
                    <Document
                        file={fileUrl}
                        onLoadSuccess={onDocumentLoadSuccess}
                    >
                        <Page pageNumber={pageNumber} />
                    </Document>
                    <div>
                        <button onClick={() => setPageNumber(pageNumber - 1)} disabled={pageNumber <= 1}>Previous</button>
                        <span>Page {pageNumber} of {numPages}</span>
                        <button onClick={() => setPageNumber(pageNumber + 1)} disabled={pageNumber >= (numPages || 1)}>Next</button>
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
