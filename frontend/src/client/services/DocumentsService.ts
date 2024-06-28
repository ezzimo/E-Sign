/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_documents_send_otp } from '../models/Body_documents_send_otp';
import type { Body_documents_update_document } from '../models/Body_documents_update_document';
import type { Body_documents_verify_otp } from '../models/Body_documents_verify_otp';
import type { DocumentOut } from '../models/DocumentOut';
import { Body_documents_create_document } from "../../client/models/Body_documents_create_document"

import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DocumentsService {

    /**
     * Create Document
     * @returns DocumentOut Successful Response
     * @throws ApiError
     */
    public static async createDocument(
        data: Body_documents_create_document,
    ): Promise<DocumentOut> {
        const formData = new FormData();
        formData.append("title", data.title);
        formData.append("status", data.status);
        if (data.file) formData.append("file", data.file);

        return __request<DocumentOut>(OpenAPI, {
            method: "POST",
            url: "/api/v1/documents/",
            body: formData,
            mediaType: "multipart/form-data",
        });
    }


    /**
     * Read Documents
     * @returns DocumentOut Successful Response
     * @throws ApiError
     */

    public static readDocuments({
        skip,
        limit = 100,
    }: {
        skip?: number,
        limit?: number,
    }): CancelablePromise<Array<DocumentOut>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/documents/',
            query: {
                'skip': skip,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Read Document
     * Get document details by ID, including download URL.
     * @returns DocumentOut Successful Response
     * @throws ApiError
     */
    public static readDocument({
        documentId,
    }: {
        documentId: number,
    }): CancelablePromise<DocumentOut> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/documents/{document_id}',
            path: {
                'document_id': documentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Update Document
     * @returns DocumentOut Successful Response
     * @throws ApiError
     */
    public static updateDocument({
        documentId,
        formData,
    }: {
        documentId: number,
        formData?: Body_documents_update_document,
    }): CancelablePromise<DocumentOut> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/documents/{document_id}',
            path: {
                'document_id': documentId,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Delete Document
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteDocument({
        documentId,
    }: {
        documentId: number,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/documents/{document_id}',
            path: {
                'document_id': documentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Download Document
     * Download the PDF file by document ID.
     * @returns any Successful Response
     * @throws ApiError
     */
    public static downloadDocument({
        documentId,
    }: {
        documentId: number,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/documents/{document_id}/download',
            path: {
                'document_id': documentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Document File
     * @returns any Successful Response
     * @throws ApiError
     */
    public static getDocumentFile({
        documentId,
    }: {
        documentId: number,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/documents/{document_id}/file',
            path: {
                'document_id': documentId,
            },
            responseType: 'blob',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Get Document File Url
     * @returns string Successful Response
     * @throws ApiError
     */
    public static getDocumentFileUrl({
        documentId,
    }: {
        documentId: number,
    }): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/documents/{document_id}/file-url',
            path: {
                'document_id': documentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Access Document With Token
     * @returns string Successful Response
     * @throws ApiError
     */
    public static accessDocumentWithToken({
        token,
    }: {
        token: string,
    }): CancelablePromise<string> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/signe/sign_document',
            query: {
                'token': token,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Send Otp
     * @returns any Successful Response
     * @throws ApiError
     */
    public static sendOtp({
        formData,
    }: {
        formData: Body_documents_send_otp,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/signe/send_otp',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }

    /**
     * Verify Otp
     * @returns any Successful Response
     * @throws ApiError
     */
    public static verifyOtp({
        formData,
    }: {
        formData: Body_documents_verify_otp,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/signe/verify_otp',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }

}
