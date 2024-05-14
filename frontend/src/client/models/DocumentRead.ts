type ReminderSettings = {
    interval_in_days: number;
    max_occurrences: number;
    timezone: string;
};

type SignatureRadio = {
    name: string;
    x: number;
    y: number;
    size: number;
};

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

type Owner = {
    email: string;
    is_active: boolean;
    is_superuser: boolean;
    id: number;
    full_name: string;
    created_at: string;
    updated_at: string;
};

export type DocumentRead = {
    id: number;
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
