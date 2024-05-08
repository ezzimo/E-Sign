import { useEffect, useState } from "react";
import { SignatureRequestRead } from "../../client/models/SignatureRequestRead";
import { fetchSignatureRequests } from "../../client/services/SignatureRequestsService";

const SignatureRequestList = () => {
	const [signatureRequests, setSignatureRequests] = useState<
		SignatureRequestRead[]
	>([]);

	useEffect(() => {
		async function loadSignatureRequests() {
			const requests = await fetchSignatureRequests();
			setSignatureRequests(requests);
		}
		loadSignatureRequests();
	}, []);

	return (
		<div>
			<h1>Signature Requests</h1>
			{signatureRequests.map((request) => (
				<div key={request.id}>
					<h2>{request.name}</h2>
					<p>Delivery Mode: {request.delivery_mode}</p>
					<p>Expiration Date: {request.expiration_date}</p>
				</div>
			))}
		</div>
	);
};

export default SignatureRequestList;
