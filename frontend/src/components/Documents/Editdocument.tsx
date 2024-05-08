import {
	Button,
	FormControl,
	FormLabel,
	Input,
	Modal,
	ModalBody,
	ModalContent,
	ModalFooter,
	ModalHeader,
	ModalOverlay,
} from "@chakra-ui/react";
import React from "react";
import { useForm } from "react-hook-form";
import { DocumentRead } from "../../client/models/DocumentRead";
import { DocumentUpdate } from "../../client/models/DocumentUpdate";
import { DocumentService } from "../../client/services/DocumentService";

interface EditDocumentProps {
	document: DocumentRead; // Ensure this matches the prop passed
	isOpen: boolean;
	onClose: () => void;
}

const EditDocument: React.FC<EditDocumentProps> = ({
	document,
	isOpen,
	onClose,
}) => {
	const {
		register,
		handleSubmit,
		formState: { errors, isSubmitting },
	} = useForm<DocumentUpdate>({
		defaultValues: {
			title: document.title,
			status: document.status,
			// Include other fields as necessary
		},
	});

	const onSubmit = async (data: DocumentUpdate) => {
		await DocumentService.updateDocument(document.id, data);
		onClose();
		// Invalidate or refetch queries as necessary
	};

	return (
		<Modal isOpen={isOpen} onClose={onClose}>
			<ModalOverlay />
			<ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
				<ModalHeader>Edit Document</ModalHeader>
				<ModalBody>
					<FormControl isInvalid={!!errors.title}>
						<FormLabel>Title</FormLabel>
						<Input id="title" {...register("title")} />
						{/* Error messages and other inputs */}
					</FormControl>
					{/* Additional inputs */}
				</ModalBody>
				<ModalFooter>
					<Button colorScheme="blue" isLoading={isSubmitting} type="submit">
						Save
					</Button>
					<Button onClick={onClose}>Cancel</Button>
				</ModalFooter>
			</ModalContent>
		</Modal>
	);
};

export default EditDocument;
