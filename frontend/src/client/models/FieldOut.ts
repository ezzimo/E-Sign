/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { FieldType } from './FieldType';
import type { RadioCreate } from './RadioCreate';

export type FieldOut = {
    type: FieldType;
    page: number;
    id: number;
    signer_id?: (number | null);
    document_id?: (number | null);
    signature_request_id?: (number | null);
    created_at: string;
    updated_at: string;
    radios?: (Array<RadioCreate> | null);
};

