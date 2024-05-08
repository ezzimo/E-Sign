import React, { ChangeEvent, useState } from "react";
import { SignatureRequestCreate } from "../../client/models/SignatureRequestCreate";
import { initiateSignatureRequest } from "../../client/services/SignatureRequestsService";

const CreateSignatureRequestForm = () => {
	const [signatureRequest, setSignatureRequest] =
		useState<SignatureRequestCreate>({
			name: "",
			delivery_mode: "",
			ordered_signers: false,
			reminder_settings: {
				interval_in_days: 0,
				max_occurrences: 0,
				timezone: "",
			},
			expiration_date: "",
			message: "",
			expiry_date: "",
			signatories: [],
			documents: [],
		});

	const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
		event.preventDefault();
		const response = await initiateSignatureRequest(signatureRequest);
		console.log("Request submitted successfully", response);
	};

	const handleInputChange = (
		event: ChangeEvent<HTMLInputElement | HTMLSelectElement>,
	) => {
		const { name, value, type } = event.target;
		if (type === "checkbox") {
			setSignatureRequest((prev) => ({
				...prev,
				[name]: (event.target as HTMLInputElement).checked,
			}));
		} else {
			setSignatureRequest((prev) => ({ ...prev, [name]: value }));
		}
	};

	return (
		<form onSubmit={handleSubmit}>
			<input
				type="text"
				name="name"
				value={signatureRequest.name}
				onChange={handleInputChange}
				placeholder="Name"
			/>
			<select
				name="delivery_mode"
				value={signatureRequest.delivery_mode}
				onChange={handleInputChange}
			>
				<option value="">Select Delivery Mode</option>
				<option value="email">Email</option>
				<option value="direct">Direct</option>
			</select>
			<label>
				Ordered Signers:
				<input
					type="checkbox"
					name="ordered_signers"
					checked={signatureRequest.ordered_signers}
					onChange={handleInputChange}
				/>
			</label>
			<button type="submit">Create Signature Request</button>
		</form>
	);
};

export default CreateSignatureRequestForm;
