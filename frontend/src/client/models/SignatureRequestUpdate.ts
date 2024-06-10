/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { ReminderSettingsSchema } from './ReminderSettingsSchema';
import type { SignatoryData } from './SignatoryData';

export type SignatureRequestUpdate = {
    name?: (string | null);
    delivery_mode?: (string | null);
    ordered_signers?: (boolean | null);
    reminder_settings?: (ReminderSettingsSchema | null);
    expiry_date?: (string | null);
    message?: (string | null);
    signatories?: (Array<SignatoryData> | null);
    documents?: (Array<number> | null);
};

