/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { AuditLogAction } from './AuditLogAction';

export type AuditLogCreate = {
    description: (string | null);
    ip_address: (string | null);
    action: AuditLogAction;
    signature_request_id: (number | null);
};

