import { Button, Flex, Icon, useDisclosure } from "@chakra-ui/react";
import type React from "react";
import { FaPlus } from "react-icons/fa";

import AddUser from "../Admin/AddUser";
import CreateDocument from "../Documents/CreateDocument";
import AddItem from "../Items/AddItem";

interface NavbarProps {
	type: string;
}

const Navbar: React.FC<NavbarProps> = ({ type }) => {
	const addUserModal = useDisclosure();
	const addItemModal = useDisclosure();
	const addDocumentModal = useDisclosure();

	const handleOpen = () => {
		if (type === "User") {
			addUserModal.onOpen();
		} else if (type === "Item") {
			addItemModal.onOpen();
		} else if (type === "Document") {
			addDocumentModal.onOpen();
		}
	};

	return (
		<>
			<Flex py={8} gap={4}>
				{/* TODO: Complete search functionality */}
				{/* <InputGroup w={{ base: '100%', md: 'auto' }}>
                    <InputLeftElement pointerEvents='none'>
                        <Icon as={FaSearch} color='gray.400' />
                    </InputLeftElement>
                    <Input type='text' placeholder='Search' fontSize={{ base: 'sm', md: 'inherit' }} borderRadius='8px' />
                </InputGroup> */}
				<Button
					variant="primary"
					gap={1}
					fontSize={{ base: "sm", md: "inherit" }}
					onClick={handleOpen}
				>
					<Icon as={FaPlus} /> Add {type}
				</Button>
				<AddUser isOpen={addUserModal.isOpen} onClose={addUserModal.onClose} />
				<AddItem isOpen={addItemModal.isOpen} onClose={addItemModal.onClose} />
				<CreateDocument
					isOpen={addDocumentModal.isOpen}
					onClose={addDocumentModal.onClose}
				/>
			</Flex>
		</>
	);
};

export default Navbar;
