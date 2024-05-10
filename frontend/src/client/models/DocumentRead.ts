// Define the reminder settings type
type ReminderSettings = {
	interval_in_days: number;
	max_occurrences: number;
	timezone: string;
  };
  
  // Define the signature radio button type
  type SignatureRadio = {
	name: string;
	x: number;
	y: number;
	size: number;
  };
  
  // Define the signature field type
  type SignatureField = {
	type: string;
	page: number;
	id: number;
	signer_id: number;
	document_id: number;
	signature_request_id: number;
	created_at: string;
	updated_at: string;
	radios: SignatureRadio[];
  };
  
  // Define the signature request type
  type SignatureRequest = {
	name: string;
	delivery_mode: string;
	ordered_signers: boolean;
	reminder_settings: ReminderSettings;
	expiration_date: string;
	message: string;
	expiry_date: string;
	id: number;
	sender_id: number;
	created_at: string;
	updated_at: string;
  };
  
  // Define the owner type
  type Owner = {
	email: string;
	is_active: boolean;
	is_superuser: boolean;
	id: number;
	full_name: string;
	created_at: string;
	updated_at: string;
  };
  
  // Define the main DocumentRead type
  export type DocumentRead = {
	id: string;
	title: string;
	file: string;
	file_url: string;
	status: string;
	created_at: string;
	updated_at: string;
	owner: Owner;
	doc_requests: SignatureRequest[];
	signature_fields: SignatureField[];
  };
  