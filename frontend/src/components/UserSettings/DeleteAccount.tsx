import {
	Button,
	Container,
	Heading,
	Text,
	useDisclosure,
} from "@chakra-ui/react";
import type React from "react";
import { useQueryClient } from "react-query";
import { UserOut } from "../../client"; // Ensure you import UserOut type

import DeleteConfirmation from "./DeleteConfirmation";

const DeleteAccount: React.FC = () => {
	const confirmationModal = useDisclosure();
	const queryClient = useQueryClient();
	const currentUser = queryClient.getQueryData<UserOut>("currentUser");

	return (
		<>
			<Container maxW="full">
				<Heading size="sm" py={4}>
					Delete Account
				</Heading>
				<Text>
					Permanently delete your data and everything associated with your
					account.
				</Text>
				<Button variant="danger" mt={4} onClick={confirmationModal.onOpen}>
					Delete
				</Button>
				{currentUser && (
					<DeleteConfirmation
						isOpen={confirmationModal.isOpen}
						onClose={confirmationModal.onClose}
						userId={currentUser.id} // Pass the current user ID here
					/>
				)}
			</Container>
		</>
	);
};
export default DeleteAccount;
