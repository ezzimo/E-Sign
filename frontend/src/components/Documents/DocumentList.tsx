import { useEffect, useState } from "react";
import { DocumentRead } from "../../client/models/DocumentRead";
import { DocumentService } from "../../client/services/DocumentService";

const DocumentList = () => {
	const [documents, setDocuments] = useState<DocumentRead[]>([]);

	useEffect(() => {
		const loadDocuments = async () => {
			const docs = await DocumentService.fetchDocuments();
			setDocuments(docs);
		};
		loadDocuments();
	}, []);

	return (
		<div>
			<h1>Documents</h1>
			{documents.map((doc) => (
				<div key={doc.id}>
					<h2>{doc.title}</h2>
					<p>Status: {doc.status}</p>
					<p>Created At: {doc.created_at}</p>
				</div>
			))}
		</div>
	);
};

export default DocumentList;
