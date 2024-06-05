/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { FieldType } from './FieldType';
import type { RadioCreate } from './RadioCreate';

export type FieldUpdate = {
    type: FieldType;
    page: number;
    'x'?: (number | null);
    'y'?: (number | null);
    height?: (number | null);
    width?: (number | null);
    optional?: (boolean | null);
    mention?: (string | null);
    name?: (string | null);
    checked?: (boolean | null);
    document_id?: (number | null);
    signature_request_id?: (number | null);
    signer_id?: (number | null);
    max_length?: (number | null);
    question?: (string | null);
    instruction?: (string | null);
    text?: (string | null);
    radios?: (Array<RadioCreate> | null);
};

