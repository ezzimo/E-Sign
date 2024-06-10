import {
	Button,
	Checkbox,
	Flex,
	FormControl,
	FormErrorMessage,
	FormLabel,
	Input,
	Modal,
	ModalBody,
	ModalCloseButton,
	ModalContent,
	ModalFooter,
	ModalHeader,
	ModalOverlay,
} from "@chakra-ui/react";
import type React from "react";
import { type SubmitHandler, useForm } from "react-hook-form";
import { useMutation, useQueryClient } from "react-query";

import {
	type ApiError,
	type UserOut,
	type UserUpdate,
	UsersService,
} from "../../client";
import useCustomToast from "../../hooks/useCustomToast";

interface EditUserProps {
	user: UserOut;
	isOpen: boolean;
	onClose: () => void;
}

interface UserUpdateForm extends UserUpdate {
	first_name: string;
	last_name: string;
}

const EditUser: React.FC<EditUserProps> = ({ user, isOpen, onClose }) => {
	const queryClient = useQueryClient();
	const showToast = useCustomToast();

	const {
		register,
		handleSubmit,
		reset,
		formState: { errors, isSubmitting, isDirty },
	} = useForm<UserUpdateForm>({
		mode: "onBlur",
		criteriaMode: "all",
		defaultValues: user,
	});

	const updateUser = async (data: UserUpdateForm) => {
		await UsersService.updateUser({ userId: user.id, requestBody: data });
	};

	const mutation = useMutation(updateUser, {
		onSuccess: () => {
			showToast("Success!", "User updated successfully.", "success");
			onClose();
		},
		onError: (err: ApiError) => {
			const errDetail = err.body?.detail;
			showToast("Something went wrong.", `${errDetail}`, "error");
		},
		onSettled: () => {
			queryClient.invalidateQueries("users");
		},
	});

	const onSubmit: SubmitHandler<UserUpdateForm> = async (data) => {
		mutation.mutate(data);
	};

	const onCancel = () => {
		reset();
		onClose();
	};

	return (
		<>
			<Modal
				isOpen={isOpen}
				onClose={onClose}
				size={{ base: "sm", md: "md" }}
				isCentered
			>
				<ModalOverlay />
				<ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
					<ModalHeader>Edit User</ModalHeader>
					<ModalCloseButton />
					<ModalBody pb={6}>
						<FormControl isInvalid={!!errors.email}>
							<FormLabel htmlFor="email">Email</FormLabel>
							<Input
								id="email"
								{...register("email", {
									required: "Email is required",
									pattern: {
										value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i,
										message: "Invalid email address",
									},
								})}
								placeholder="Email"
								type="email"
							/>
							{errors.email && (
								<FormErrorMessage>{errors.email.message}</FormErrorMessage>
							)}
						</FormControl>
						<FormControl mt={4}>
							<FormLabel htmlFor="name">Full name</FormLabel>
							<Input id="name" {...register("full_name")} type="text" />
						</FormControl>
						<FormControl mt={4}>
							<FormLabel htmlFor="first_name">First Name</FormLabel>
							<Input
								id="first_name"
								{...register("first_name", {
									required: "First name is required",
								})}
								placeholder="First Name"
								type="text"
							/>
							{errors.first_name && (
								<FormErrorMessage>{errors.first_name.message}</FormErrorMessage>
							)}
						</FormControl>
						<FormControl mt={4}>
							<FormLabel htmlFor="last_name">Last Name</FormLabel>
							<Input
								id="last_name"
								{...register("last_name", {
									required: "Last name is required",
								})}
								placeholder="Last Name"
								type="text"
							/>
							{errors.last_name && (
								<FormErrorMessage>{errors.last_name.message}</FormErrorMessage>
							)}
						</FormControl>
						<Flex>
							<FormControl mt={4}>
								<Checkbox {...register("is_superuser")} colorScheme="teal">
									Is superuser?
								</Checkbox>
							</FormControl>
							<FormControl mt={4}>
								<Checkbox {...register("is_active")} colorScheme="teal">
									Is active?
								</Checkbox>
							</FormControl>
						</Flex>
					</ModalBody>

					<ModalFooter gap={3}>
						<Button
							variant="primary"
							type="submit"
							isLoading={isSubmitting}
							isDisabled={!isDirty}
						>
							Save
						</Button>
						<Button onClick={onCancel}>Cancel</Button>
					</ModalFooter>
				</ModalContent>
			</Modal>
		</>
	);
};

export default EditUser;
