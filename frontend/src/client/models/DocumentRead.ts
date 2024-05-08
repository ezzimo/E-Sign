export type DocumentRead = {
	[x: string]: string;
	id: number;
	title: string;
	file: string;
	status: string;
	created_at: string;
	updated_at: string;
	owner: {
		email: string;
		is_active: boolean;
		is_superuser: boolean;
		id: number;
		full_name: string;
		created_at: string;
		updated_at: string;
	};
	doc_requests: Array<{
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
		id: number;
		sender_id: number;
		created_at: string;
		updated_at: string;
	}>;
	signature_fields: Array<{
		type: string;
		page: number;
		id: number;
		signer_id: number;
		document_id: number;
		signature_request_id: number;
		created_at: string;
		updated_at: string;
		radios: Array<{
			name: string;
			x: number;
			y: number;
			size: number;
		}>;
	}>;
};
