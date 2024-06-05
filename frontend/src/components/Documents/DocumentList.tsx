import { useEffect, useState } from "react";
import { DocumentOut } from "../../client/models/DocumentOut";
import { DocumentsService } from "../../client/services/DocumentsService";

const DocumentList = () => {
	const [documents, setDocuments] = useState<DocumentOut[]>([]);

	useEffect(() => {
		const loadDocuments = async () => {
			const docs = await DocumentsService.readDocuments({ skip: 0, limit: 100 });
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
