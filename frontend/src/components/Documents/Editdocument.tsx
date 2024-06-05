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
import { DocumentOut } from "../../client/models/DocumentOut";
import { Body_documents_update_document } from "../../client/models/Body_documents_update_document";
import { DocumentsService } from "../../client/services/DocumentsService";

interface EditDocumentProps {
	document: DocumentOut;
	isOpen: boolean;
	onClose: () => void;
}

const EditDocument: React.FC<EditDocumentProps> = ({ document, isOpen, onClose }) => {
	const { register, handleSubmit, formState: { errors, isSubmitting } } = useForm<Body_documents_update_document>({
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

	const onSubmit = async (data: Body_documents_update_document) => {
		const formData = {
			...data,
			file: newFile,  // Assuming you want to include file updates
		};
		await DocumentsService.updateDocument({ documentId: document.id, formData });
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
