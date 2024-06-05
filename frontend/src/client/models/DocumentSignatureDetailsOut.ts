/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type DocumentSignatureDetailsOut = {
    document_id: number;
    /**
     * SHA-256 hash of the signed document
     */
    signed_hash: string;
    /**
     * The time when the document was signed
     */
    timestamp: string;
    /**
     * Certified timestamp if available
     */
    certified_timestamp?: (string | null);
    /**
     * IP address of the signer
     */
    ip_address?: (string | null);
    id: number;
};

