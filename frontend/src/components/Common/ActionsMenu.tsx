import React, { useState } from "react";
import {
    Button,
    Menu,
    MenuButton,
    MenuItem,
    MenuList,
    useDisclosure,
    Modal,
    ModalOverlay,
    ModalContent,
    ModalHeader,
    ModalBody,
    ModalCloseButton,
    useToast
} from "@chakra-ui/react";
import { BsThreeDotsVertical } from "react-icons/bs";
import { FiEdit, FiTrash, FiEye } from "react-icons/fi";
import { ItemOut, UserOut } from "../../client";
import { DocumentRead } from "../../client/models/DocumentRead";
import { SignatureRequestRead } from "../../client/models/SignatureRequestRead";
import EditUser from "../Admin/EditUser";
import EditDocument from "../Documents/Editdocument";
import EditItem from "../Items/EditItem";
import DeleteAlert from "./DeleteAlert";
import DocumentViewer from "../Documents/DocumentViewer";
import { DocumentService } from "../../client/services/DocumentService";

interface ActionsMenuProps {
    type: string;
    value: ItemOut | UserOut | DocumentRead | SignatureRequestRead;
    disabled?: boolean;
}

const ActionsMenu: React.FC<ActionsMenuProps> = ({ type, value, disabled }) => {
    const editModal = useDisclosure();
    const deleteModal = useDisclosure();
    const viewModal = useDisclosure();
    const toast = useToast();

    const [documentDetails, setDocumentDetails] = useState<DocumentRead | null>(null);
    const [fileBlob, setFileBlob] = useState<Blob | null>(null);

    const handleDelete = async () => {
        try {
            if (type === "Document") {
                await DocumentService.deleteDocument(value.id as number);
                toast({
                    title: "Document deleted.",
                    description: "The document has been deleted successfully.",
                    status: "success",
                    duration: 5000,
                    isClosable: true,
                });
            }
        } catch (error) {
            toast({
                title: "Error deleting document.",
                description: "An error occurred while deleting the document.",
                status: "error",
                duration: 5000,
                isClosable: true,
            });
        } finally {
            deleteModal.onClose();
        }
    };

    const handleViewDocument = async () => {
        try {
            const details = await DocumentService.fetchDocumentById(value.id as number);
            setDocumentDetails(details);
    
            // Fetch the document file blob
            const file = await DocumentService.fetchDocumentFile(value.id as number);
            setFileBlob(file);
    
            viewModal.onOpen();
        } catch (error) {
            toast({
                title: "Error viewing document.",
                description: "An error occurred while fetching the document.",
                status: "error",
                duration: 5000,
                isClosable: true,
            });
        }
    };

    const renderEditModal = () => {
        switch (type) {
            case "User":
                return (
                    <EditUser
                        user={value as UserOut}
                        isOpen={editModal.isOpen}
                        onClose={editModal.onClose}
                    />
                );
            case "Item":
                return (
                    <EditItem
                        item={value as ItemOut}
                        isOpen={editModal.isOpen}
                        onClose={editModal.onClose}
                    />
                );
            case "Document":
                return (
                    <EditDocument
                        document={value as DocumentRead}
                        isOpen={editModal.isOpen}
                        onClose={editModal.onClose}
                    />
                );
            default:
                return null;
        }
    };

    return (
        <>
            <Menu>
                <MenuButton
                    as={Button}
                    rightIcon={<BsThreeDotsVertical />}
                    variant="ghost"
                    isDisabled={disabled}
                >
                    Actions
                </MenuButton>
                <MenuList>
                    <MenuItem icon={<FiEye />} onClick={handleViewDocument}>
                        View {type}
                    </MenuItem>
                    <MenuItem icon={<FiEdit />} onClick={editModal.onOpen}>
                        Edit {type}
                    </MenuItem>
                    <MenuItem
                        icon={<FiTrash />}
                        color="red.500"
                        onClick={deleteModal.onOpen}
                    >
                        Delete {type}
                    </MenuItem>
                </MenuList>
                {renderEditModal()}
                <DeleteAlert
                    isOpen={deleteModal.isOpen}
                    onClose={deleteModal.onClose}
                    id={Number(value.id)}
                    type={type}
                    onDelete={handleDelete}
                />
            </Menu>

            <Modal isOpen={viewModal.isOpen} onClose={viewModal.onClose} size="xl">
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>View Document</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody>
                        {type === "Document" && documentDetails && fileBlob && (
                            <DocumentViewer
                                documentDetails={documentDetails}
                                fileBlob={fileBlob}
                                fileType="application/pdf"
                            />
                        )}
                    </ModalBody>
                </ModalContent>
            </Modal>
        </>
    );
};

export default ActionsMenu;
