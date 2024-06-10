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
import { useMutation, useQueryClient } from "react-query";
import { type ApiError, UsersService } from "../../client";
import useCustomToast from "../../hooks/useCustomToast";

interface DeleteProps {
	isOpen: boolean;
	onClose: () => void;
	userId: number; // Accept the user ID as a prop
}

const DeleteConfirmation: React.FC<DeleteProps> = ({
	isOpen,
	onClose,
	userId,
}) => {
	const queryClient = useQueryClient();
	const showToast = useCustomToast();
	const cancelRef = React.useRef<HTMLButtonElement | null>(null);
	const {
		handleSubmit,
		formState: { isSubmitting },
	} = useForm();

	const deleteUser = async (id: number) => {
		await UsersService.deleteUser({ userId: id });
	};

	const mutation = useMutation(() => deleteUser(userId), {
		onSuccess: () => {
			showToast(
				"Success",
				"The user has been successfully deleted.",
				"success",
			);
			queryClient.invalidateQueries("users");
			onClose();
		},
		onError: (err: ApiError) => {
			const errDetail = err.body?.detail;
			showToast("Something went wrong.", `${errDetail}`, "error");
		},
	});

	const onSubmit = async () => {
		mutation.mutate();
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
						<AlertDialogHeader>Confirmation Required</AlertDialogHeader>

						<AlertDialogBody>
							All user data will be <strong>permanently deleted.</strong> If you
							are sure, please click <strong>"Confirm"</strong> to proceed. This
							action cannot be undone.
						</AlertDialogBody>

						<AlertDialogFooter gap={3}>
							<Button variant="danger" type="submit" isLoading={isSubmitting}>
								Confirm
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

export default DeleteConfirmation;
