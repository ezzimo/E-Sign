// frontend/src/components/Common/ActionsMenu.tsx

import React from "react";
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
import EditUser from "../Admin/EditUser";
import EditDocument from "../Documents/Editdocument";
import EditItem from "../Items/EditItem";
import DeleteAlert from "./DeleteAlert";
import { DocumentViewer } from "../Documents/DocumentViewer"; // Import as named export
import { DocumentService } from "../../client/services/DocumentService";

interface ActionsMenuProps {
    type: string;
    value: ItemOut | UserOut | DocumentRead;
    disabled?: boolean;
}

const ActionsMenu: React.FC<ActionsMenuProps> = ({ type, value, disabled }) => {
    const editModal = useDisclosure();
    const deleteModal = useDisclosure();
    const viewModal = useDisclosure();
    const toast = useToast();

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
                    <MenuItem icon={<FiEye />} onClick={viewModal.onOpen}>
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
                    onDelete={handleDelete} // Pass the delete handler
                />
            </Menu>

            {/* Modal to display the DocumentViewer */}
            <Modal isOpen={viewModal.isOpen} onClose={viewModal.onClose} size="xl">
                <ModalOverlay />
                <ModalContent>
                    <ModalHeader>View {type}</ModalHeader>
                    <ModalCloseButton />
                    <ModalBody>
                        {type === "Document" && (
                            <DocumentViewer
                                documentID={value.id as number}
                            />
                        )}
                    </ModalBody>
                </ModalContent>
            </Modal>
        </>
    );
};

export default ActionsMenu;
