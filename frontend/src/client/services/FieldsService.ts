/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { FieldCreate } from '../models/FieldCreate';
import type { FieldOut } from '../models/FieldOut';
import type { FieldUpdate } from '../models/FieldUpdate';

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class FieldsService {

    /**
     * Create Field Endpoint
     * @returns FieldOut Successful Response
     * @throws ApiError
     */
    public static createFieldEndpoint({
        signatureRequestId,
        documentId,
        requestBody,
    }: {
        signatureRequestId: number,
        documentId: number,
        requestBody: FieldCreate,
    }): CancelablePromise<FieldOut> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/fields/{signature_request_id}/documents/{document_id}/fields',
            path: {
                'signature_request_id': signatureRequestId,
                'document_id': documentId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Field
     * @returns FieldOut Successful Response
     * @throws ApiError
     */
    public static readField({
        fieldId,
    }: {
        fieldId: number,
    }): CancelablePromise<FieldOut> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/fields/{field_id}',
            path: {
                'field_id': fieldId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Field Endpoint
     * @returns FieldOut Successful Response
     * @throws ApiError
     */
    public static updateFieldEndpoint({
        fieldId,
        requestBody,
    }: {
        fieldId: number,
        requestBody: FieldUpdate,
    }): CancelablePromise<FieldOut> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/fields/{field_id}',
            path: {
                'field_id': fieldId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Field Endpoint
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteFieldEndpoint({
        fieldId,
    }: {
        fieldId: number,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/fields/{field_id}',
            path: {
                'field_id': fieldId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
