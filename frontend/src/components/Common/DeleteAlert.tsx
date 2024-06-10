import {
	AlertDialog,
	AlertDialogBody,
	AlertDialogContent,
	AlertDialogFooter,
	AlertDialogHeader,
	AlertDialogOverlay,
	Button,
} from "@chakra-ui/react";
import React from "react";
import { useForm } from "react-hook-form";
import { useQueryClient } from "react-query";

import useCustomToast from "../../hooks/useCustomToast";

interface DeleteProps {
	type: string;
	id: number;
	isOpen: boolean;
	onClose: () => void;
	onDelete: () => Promise<void>; // Add this prop for the delete handler
}

const DeleteAlert: React.FC<DeleteProps> = ({ type, isOpen, onClose, onDelete }) => {
	const queryClient = useQueryClient();
	const showToast = useCustomToast();
	const cancelRef = React.useRef<HTMLButtonElement | null>(null);
	const {
			handleSubmit,
			formState: { isSubmitting },
	} = useForm();

	const onSubmit = async () => {
			try {
					await onDelete(); // Use the onDelete prop here
					showToast(
							"Success",
							`The ${type.toLowerCase()} was deleted successfully.`,
							"success"
					);
					queryClient.invalidateQueries(type.toLowerCase());
					onClose();
			} catch (error) {
					showToast(
							"An error occurred.",
							`An error occurred while deleting the ${type.toLowerCase()}.`,
							"error"
					);
			}
	};

	return (
			<>
					<AlertDialog
							isOpen={isOpen}
							onClose={onClose}
							leastDestructiveRef={cancelRef}
							size={{ base: "sm", md: "md" }}
							isCentered
					>
							<AlertDialogOverlay>
									<AlertDialogContent as="form" onSubmit={handleSubmit(onSubmit)}>
											<AlertDialogHeader>Delete {type}</AlertDialogHeader>

											<AlertDialogBody>
													{type === "User" && (
															<span>
																	All items associated with this user will also be{" "}
																	<strong>permanently deleted. </strong>
															</span>
													)}
													Are you sure? You will not be able to undo this action.
											</AlertDialogBody>

											<AlertDialogFooter gap={3}>
													<Button variant="danger" type="submit" isLoading={isSubmitting}>
															Delete
													</Button>
													<Button
															ref={cancelRef}
															onClick={onClose}
															isDisabled={isSubmitting}
													>
															Cancel
													</Button>
											</AlertDialogFooter>
									</AlertDialogContent>
							</AlertDialogOverlay>
					</AlertDialog>
			</>
	);
};

export default DeleteAlert;
