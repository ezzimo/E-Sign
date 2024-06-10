/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { SignatoryCreate } from '../models/SignatoryCreate';
import type { SignatoryOut } from '../models/SignatoryOut';
import type { SignatoryUpdate } from '../models/SignatoryUpdate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class SignatoriesService {

    /**
     * Create Signatory
     * Create a new signatory with the specified user as the creator.
     * Automatically attempts to link a signer by email.
     * @returns SignatoryOut Successful Response
     * @throws ApiError
     */
    public static createSignatory({
        requestBody,
    }: {
        requestBody: SignatoryCreate,
    }): CancelablePromise<SignatoryOut> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/signatories/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Signatory
     * Read a signatory by its ID.
     * @returns SignatoryOut Successful Response
     * @throws ApiError
     */
    public static readSignatory({
        signatoryId,
    }: {
        signatoryId: number,
    }): CancelablePromise<SignatoryOut> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/signatories/{signatory_id}',
            path: {
                'signatory_id': signatoryId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Signatory
     * Update a signatory's information.
     * @returns SignatoryOut Successful Response
     * @throws ApiError
     */
    public static updateSignatory({
        signatoryId,
        requestBody,
    }: {
        signatoryId: number,
        requestBody: SignatoryUpdate,
    }): CancelablePromise<SignatoryOut> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/signatories/{signatory_id}',
            path: {
                'signatory_id': signatoryId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Signatory
     * Delete a signatory from the database.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteSignatory({
        signatoryId,
    }: {
        signatoryId: number,
    }): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/signatories/{signatory_id}',
            path: {
                'signatory_id': signatoryId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Signatories By Document
     * Read signatories associated with a specific document.
     * @returns SignatoryOut Successful Response
     * @throws ApiError
     */
    public static readSignatoriesByDocument({
        documentId,
    }: {
        documentId: number,
    }): CancelablePromise<Array<SignatoryOut>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/signatories/document/{document_id}',
            path: {
                'document_id': documentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
