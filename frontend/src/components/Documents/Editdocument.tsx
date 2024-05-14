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
	ModalOverlay
} from "@chakra-ui/react";
import React, { useState } from "react";
import { useForm } from "react-hook-form";
import { DocumentRead } from "../../client/models/DocumentRead";
import { DocumentUpdate } from "../../client/models/DocumentUpdate";
import { DocumentService } from "../../client/services/DocumentService";

interface EditDocumentProps {
	document: DocumentRead;
	isOpen: boolean;
	onClose: () => void;
}

const EditDocument: React.FC<EditDocumentProps> = ({ document, isOpen, onClose }) => {
	const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<DocumentUpdate>({
			defaultValues: {
					title: document.title,
					status: document.status,
			},
	});

	const [newFile, setNewFile] = useState<File | null>(null);

	const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
			const file = event.target.files ? event.target.files[0] : null;
			setNewFile(file);
	};

	const onSubmit = async (data: DocumentUpdate) => {
			const updateData = { ...data, file: newFile };
			await DocumentService.updateDocument(document.id, updateData);
			onClose();
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
									</FormControl>
									<FormControl>
											<FormLabel>File</FormLabel>
											<Input type="file" onChange={handleFileChange} />
									</FormControl>
							</ModalBody>
							<ModalFooter>
									<Button isLoading={isSubmitting} type="submit">
											Save Changes
									</Button>
									<Button onClick={onClose}>Cancel</Button>
							</ModalFooter>
					</ModalContent>
			</Modal>
	);
};

export default EditDocument;
