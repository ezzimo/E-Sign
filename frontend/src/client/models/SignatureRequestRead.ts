export interface SignatureRequestRead {
	id: number;
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
	sender_id: number;
	created_at: string;
	updated_at: string;
}
