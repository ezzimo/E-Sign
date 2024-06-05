/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { DocumentSignatureDetailsOut } from './DocumentSignatureDetailsOut';
import type { DocumentStatus } from './DocumentStatus';
import type { UserOut } from './UserOut';

export type DocumentOut = {
    /**
     * Title of the document
     */
    title: string;
    /**
     * File path or identifier
     */
    file: string;
    /**
     * URL to view the document
     */
    file_url?: (string | null);
    /**
     * Current status of the document
     */
    status: DocumentStatus;
    /**
     * Unique identifier for the document
     */
    id: number;
    /**
     * Timestamp when the document was created
     */
    created_at: string;
    /**
     * Timestamp when the document was last updated
     */
    updated_at: string;
    /**
     * User information of the owner
     */
    owner: UserOut;
    signature_details?: (DocumentSignatureDetailsOut | null);
};

