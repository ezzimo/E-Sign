import {
	Button,
	Menu,
	MenuButton,
	MenuItem,
	MenuList,
	Modal,
	ModalBody,
	ModalCloseButton,
	ModalContent,
	ModalHeader,
	ModalOverlay,
	useDisclosure,
	useToast,
} from "@chakra-ui/react";
import React, { useState } from "react";
import { BsThreeDotsVertical } from "react-icons/bs";
import { FiEdit, FiEye, FiTrash } from "react-icons/fi";
import { ItemOut, UserOut } from "../../client";
import { DocumentOut } from "../../client/models/DocumentOut";
import { SignatureRequestRead } from "../../client/models/SignatureRequestRead";
import { DocumentsService } from "../../client/services/DocumentsService";
import { UsersService } from "../../client/services/UsersService";
import EditUser from "../Admin/EditUser";
import DocumentViewer from "../Documents/DocumentViewer";
import EditDocument from "../Documents/Editdocument";
import EditItem from "../Items/EditItem";
import DeleteConfirmation from "../UserSettings/DeleteConfirmation";
import DeleteAlert from "./DeleteAlert";

interface ActionsMenuProps {
	type: string;
	value: ItemOut | UserOut | DocumentOut | SignatureRequestRead;
	disabled?: boolean;
}

const ActionsMenu: React.FC<ActionsMenuProps> = ({ type, value, disabled }) => {
	const editModal = useDisclosure();
	const deleteModal = useDisclosure();
	const viewModal = useDisclosure();
	const toast = useToast();

	const [documentDetails, setDocumentDetails] = useState<DocumentOut | null>(
		null,
	);
	const [fileBlob, setFileBlob] = useState<Blob | null>(null);

	const handleDelete = async () => {
		try {
			if (type === "Document") {
				await DocumentsService.deleteDocument({
					documentId: value.id as number,
				});
				toast({
					title: "Document deleted.",
					description: "The document has been deleted successfully.",
					status: "success",
					duration: 5000,
					isClosable: true,
				});
			} else if (type === "User") {
				await UsersService.deleteUser({ userId: value.id as number });
				toast({
					title: "User deleted.",
					description: "The user has been deleted successfully.",
					status: "success",
					duration: 5000,
					isClosable: true,
				});
			}
			deleteModal.onClose();
		} catch (error) {
			toast({
				title: `Error deleting ${type.toLowerCase()}.`,
				description: `An error occurred while deleting the ${type.toLowerCase()}.`,
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
			const details = await DocumentsService.getDocumentFile({
				documentId: value.id as number,
			});
			setDocumentDetails(details);

			// Fetch the document file blob
			const file = await DocumentsService.getDocumentFile({
				documentId: value.id as number,
			});
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
						document={value as DocumentOut}
						isOpen={editModal.isOpen}
						onClose={editModal.onClose}
					/>
				);
			default:
				return null;
		}
	};

	const renderDeleteModal = () => {
		if (type === "User") {
			return (
				<DeleteConfirmation
					userId={value.id as number} // Pass the user ID here
					isOpen={deleteModal.isOpen}
					onClose={deleteModal.onClose}
				/>
			);
		}
		return (
			<DeleteAlert
				isOpen={deleteModal.isOpen}
				onClose={deleteModal.onClose}
				id={Number(value.id)}
				type={type}
				onDelete={handleDelete}
			/>
		);
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
				{renderDeleteModal()}
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
