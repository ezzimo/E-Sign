import {
	Button,
	Menu,
	MenuButton,
	MenuItem,
	MenuList,
	useDisclosure,
} from "@chakra-ui/react";
import { BsThreeDotsVertical } from "react-icons/bs";
import { FiEdit, FiTrash } from "react-icons/fi";

import { ItemOut, UserOut } from "../../client";
import { DocumentRead } from "../../client/models/DocumentRead";
import EditUser from "../Admin/EditUser";
import EditDocument from "../Documents/Editdocument";
import EditItem from "../Items/EditItem";
import DeleteAlert from "./DeleteAlert";

interface ActionsMenuProps {
	type: string;
	value: ItemOut | UserOut | DocumentRead;
	disabled?: boolean;
}

const ActionsMenu: React.FC<ActionsMenuProps> = ({ type, value, disabled }) => {
	const editModal = useDisclosure();
	const deleteModal = useDisclosure();

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
					id={value.id}
					type={type}
				/>
			</Menu>
		</>
	);
};

export default ActionsMenu;
