/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SignatoryOut } from '../models/SignatoryOut';
import type { SignatureRequestCreate } from '../models/SignatureRequestCreate';
import type { SignatureRequestRead } from '../models/SignatureRequestRead';
import type { SignatureRequestUpdate } from '../models/SignatureRequestUpdate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SignatureRequestsService {

    /**
     * List Signature Requests
     * List all signature requests for the admin or the current user.
     * @returns SignatureRequestRead Successful Response
     * @throws ApiError
     */
    public static listSignatureRequests(): CancelablePromise<Array<SignatureRequestRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/signature_requests/',
        });
    }

    /**
     * Initiate Signature Request
     * Initiate a new signature request.
     * @returns SignatureRequestRead Successful Response
     * @throws ApiError
     */
    public static initiateSignatureRequest({
        requestBody,
    }: {
        requestBody: SignatureRequestCreate,
    }): CancelablePromise<SignatureRequestRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/signature_requests/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Request
     * Get a signature request by ID.
     * @returns SignatureRequestRead Successful Response
     * @throws ApiError
     */
    public static readRequest({
        requestId,
    }: {
        requestId: number,
    }): CancelablePromise<SignatureRequestRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/signature_requests/{request_id}',
            path: {
                'request_id': requestId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Request
     * Update a signature request.
     * @returns SignatureRequestRead Successful Response
     * @throws ApiError
     */
    public static updateRequest({
        requestId,
        requestBody,
    }: {
        requestId: number,
        requestBody: SignatureRequestUpdate,
    }): CancelablePromise<SignatureRequestRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/signature_requests/{request_id}',
            path: {
                'request_id': requestId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Request
     * Delete a signature request.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteRequest({
        requestId,
    }: {
        requestId: number,
    }): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/signature_requests/{request_id}',
            path: {
                'request_id': requestId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Requests By Document
     * Get all signature requests for a specific document.
     * @returns SignatureRequestRead Successful Response
     * @throws ApiError
     */
    public static readRequestsByDocument({
        documentId,
    }: {
        documentId: number,
    }): CancelablePromise<Array<SignatureRequestRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/signature_requests/document/{document_id}',
            path: {
                'document_id': documentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * List Signature Request Signers
     * List all signatories for a specific signature request.
     * @returns SignatoryOut Successful Response
     * @throws ApiError
     */
    public static listSignatureRequestSigners({
        requestId,
    }: {
        requestId: number,
    }): CancelablePromise<Array<SignatoryOut>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/signature_requests/signature-request/{request_id}/signers',
            path: {
                'request_id': requestId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
