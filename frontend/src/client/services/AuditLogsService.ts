/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AuditLogCreate } from '../models/AuditLogCreate';
import type { AuditLogRead } from '../models/AuditLogRead';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class AuditLogsService {

    /**
     * Create Audit Log Endpoint
     * @returns AuditLogRead Successful Response
     * @throws ApiError
     */
    public static createAuditLogEndpoint({
        requestBody,
    }: {
        requestBody: AuditLogCreate,
    }): CancelablePromise<AuditLogRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/audit_logs/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Audit Logs For Document
     * @returns AuditLogRead Successful Response
     * @throws ApiError
     */
    public static getAuditLogsForDocument({
        documentId,
    }: {
        documentId: number,
    }): CancelablePromise<Array<AuditLogRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/audit_logs/document/{document_id}',
            path: {
                'document_id': documentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
