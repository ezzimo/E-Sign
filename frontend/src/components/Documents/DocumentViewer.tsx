import React, { useEffect, useState, useRef } from "react";
import { DocumentService } from "../../client/services/DocumentService";
import { DocumentRead } from "../../client/models/DocumentRead";

interface DocumentViewerProps {
    documentID: number;
}

export const DocumentViewer: React.FC<DocumentViewerProps> = ({ documentID }) => {
    const [document, setDocument] = useState<DocumentRead | null>(null);
    const iframeRef = useRef<HTMLIFrameElement>(null);

    useEffect(() => {
        const fetchDocument = async () => {
            try {
                const fetchedDocument = await DocumentService.fetchDocumentById(documentID);
                setDocument(fetchedDocument);
            } catch (error) {
                console.error("Error fetching document:", error);
            }
        };

        fetchDocument();
    }, [documentID]);

    useEffect(() => {
        const fetchDocumentFile = async () => {
            try {
                const response = await DocumentService.fetchDocumentFile(documentID);
                const blob = await response.blob();
                const url = URL.createObjectURL(blob);
                if (iframeRef.current) {
                    iframeRef.current.src = url;
                }
            } catch (error) {
                console.error("Error fetching document file:", error);
            }
        };

        fetchDocumentFile();
    }, [documentID]);

    if (!document) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h3>{document.title}</h3>
            <iframe ref={iframeRef} width="100%" height="600px" />
        </div>
    );
};
