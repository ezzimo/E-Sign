/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ReminderSettingsSchema } from './ReminderSettingsSchema';
import type { SignatoryData } from './SignatoryData';

export type SignatureRequestCreate = {
    name: string;
    delivery_mode: string;
    ordered_signers: boolean;
    reminder_settings?: (ReminderSettingsSchema | null);
    expiry_date?: (string | null);
    message?: (string | null);
    signatories: Array<SignatoryData>;
    documents: Array<number>;
};

