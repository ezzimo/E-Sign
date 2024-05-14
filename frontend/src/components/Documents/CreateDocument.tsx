import {
	Button,
	Input,
	Modal,
	ModalBody,
	ModalCloseButton,
	ModalContent,
	ModalFooter,
	ModalHeader,
	ModalOverlay,
	FormControl,
	FormLabel
} from "@chakra-ui/react";
import React, { ChangeEvent, useState } from "react";
import { useForm } from "react-hook-form";
import { DocumentCreate } from "../../client/models/DocumentCreate";
import { DocumentService } from "../../client/services/DocumentService";

interface CreateDocumentProps {
	isOpen: boolean;
	onClose: () => void;
}

const CreateDocument: React.FC<CreateDocumentProps> = ({ isOpen, onClose }) => {
	const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<DocumentCreate>();

	const [file, setFile] = useState<File | null>(null);

	const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
			const file = event.target.files ? event.target.files[0] : null;
			setFile(file);
	};

	const onSubmit = async (data: DocumentCreate) => {
			if (file) {
					await DocumentService.createDocument({ ...data, file });
					onClose();
			}
	};

	return (
			<Modal isOpen={isOpen} onClose={onClose}>
					<ModalOverlay />
					<ModalContent as="form" onSubmit={handleSubmit(onSubmit)}>
							<ModalHeader>Create Document</ModalHeader>
							<ModalCloseButton />
							<ModalBody>
									<FormControl isInvalid={!!errors.title}>
											<FormLabel>Title</FormLabel>
											<Input id="title" {...register("title", { required: "Title is required" })} />
									</FormControl>
									<FormControl isInvalid={!!errors.status}>
											<FormLabel>Status</FormLabel>
											<Input id="status" {...register("status", { required: "Status is required" })} />
									</FormControl>
									<FormControl>
											<FormLabel>File</FormLabel>
											<Input type="file" onChange={handleFileChange} />
									</FormControl>
							</ModalBody>
							<ModalFooter>
									<Button colorScheme="blue" mr={3} onClick={onClose}>
											Close
									</Button>
									<Button isLoading={isSubmitting} type="submit" variant="ghost">
											Upload Document
									</Button>
							</ModalFooter>
					</ModalContent>
			</Modal>
	);
};

export default CreateDocument;
