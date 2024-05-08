export type SignatureRequestCreate = {
	name: string;
	delivery_mode: string;
	ordered_signers: boolean;
	reminder_settings: {
		interval_in_days: number;
		max_occurrences: number;
		timezone: string;
	};
	expiration_date: string;
	message: string;
	expiry_date: string;
	signatories: Array<{
		info: {
			first_name: string;
			last_name: string;
			email: string;
			phone_number: string;
			signing_order: number;
			role: string;
		};
		fields: Array<{
			type: string;
			page: number;
			signer_id: number;
			document_id: string;
			x: number;
			y: number;
			height: number;
			width: number;
			optional: boolean;
			mention: string;
			name: string;
			checked: boolean;
			max_length: number;
			question: string;
			instruction: string;
			text: string;
			radios: Array<{
				name: string;
				x: number;
				y: number;
				size: number;
			}>;
		}>;
	}>;
	documents: number[];
};
