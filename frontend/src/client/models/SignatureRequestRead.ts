/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { DocumentOut } from './DocumentOut';
import type { ReminderSettingsSchema } from './ReminderSettingsSchema';
import type { SignatoryOut } from './SignatoryOut';
import type { SignatureRequestStatus } from './SignatureRequestStatus';

export type SignatureRequestRead = {
    name: string;
    delivery_mode: string;
    ordered_signers: boolean;
    reminder_settings?: (ReminderSettingsSchema | null);
    expiry_date?: (string | null);
    message?: (string | null);
    id: number;
    status: SignatureRequestStatus;
    sender_id: number;
    created_at: string;
    updated_at: string;
    documents: Array<DocumentOut>;
    signatories: Array<SignatoryOut>;
};

