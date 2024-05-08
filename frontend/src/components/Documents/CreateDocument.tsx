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
} from "@chakra-ui/react";
import React, { ChangeEvent, useState } from "react";
import { DocumentCreate } from "../../client/models/DocumentCreate";
import { DocumentService } from "../../client/services/DocumentService";

interface CreateDocumentProps {
	isOpen: boolean;
	onClose: () => void;
}

const CreateDocument: React.FC<CreateDocumentProps> = ({ isOpen, onClose }) => {
	const [document, setDocument] = useState<DocumentCreate>({
		title: "",
		status: "",
		file: null,
	});

	const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
		event.preventDefault();
		if (document.file) {
			await DocumentService.createDocument(document);
			onClose(); // Close modal on successful creation
		}
	};

	const handleFileChange = (event: ChangeEvent<HTMLInputElement>) => {
		const file = event.target.files ? event.target.files[0] : null;
		setDocument((prev) => ({ ...prev, file }));
	};

	return (
		<Modal isOpen={isOpen} onClose={onClose}>
			<ModalOverlay />
			<ModalContent as="form" onSubmit={handleSubmit}>
				<ModalHeader>Create Document</ModalHeader>
				<ModalCloseButton />
				<ModalBody>
					<label>
						Title:
						<Input
							type="text"
							value={document.title}
							onChange={(e) =>
								setDocument({ ...document, title: e.target.value })
							}
						/>
					</label>
					<label>
						Status:
						<Input
							type="text"
							value={document.status}
							onChange={(e) =>
								setDocument({ ...document, status: e.target.value })
							}
						/>
					</label>
					<label>
						File:
						<input type="file" onChange={handleFileChange} />
					</label>
				</ModalBody>
				<ModalFooter>
					<Button colorScheme="blue" mr={3} onClick={onClose}>
						Close
					</Button>
					<Button variant="ghost" type="submit">
						Upload Document
					</Button>
				</ModalFooter>
			</ModalContent>
		</Modal>
	);
};

export default CreateDocument;
