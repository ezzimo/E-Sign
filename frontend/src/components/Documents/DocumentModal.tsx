import React from "react";
import { Modal, ModalOverlay, ModalContent, ModalHeader, ModalCloseButton, ModalBody, ModalFooter, Button } from "@chakra-ui/react";
import DocumentViewer from "../Documents/DocumentViewer";
import { DocumentOut } from "../../client/models/DocumentOut";

interface DocumentModalProps {
    isOpen: boolean;
    onClose: () => void;
    documentDetails: DocumentOut | null;
    fileBlob: Blob | null;
}

const DocumentModal: React.FC<DocumentModalProps> = ({ isOpen, onClose, documentDetails, fileBlob }) => {
    return (
        <Modal isOpen={isOpen} onClose={onClose} size="full">
            <ModalOverlay />
            <ModalContent>
                <ModalHeader>View Document</ModalHeader>
                <ModalCloseButton />
                <ModalBody>
                    {documentDetails && fileBlob && (
                        <div style={{ height: '100vh', overflow: 'hidden' }}>
                            <DocumentViewer
                                documentDetails={documentDetails}
                                fileBlob={fileBlob}
                                fileType="application/pdf"
                            />
                        </div>
                    )}
                </ModalBody>
                <ModalFooter>
                    <Button colorScheme="blue" onClick={onClose}>
                        Close
                    </Button>
                </ModalFooter>
            </ModalContent>
        </Modal>
    );
};

export default DocumentModal;
