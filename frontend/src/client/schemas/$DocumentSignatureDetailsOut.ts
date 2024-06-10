/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $DocumentSignatureDetailsOut = {
    properties: {
        document_id: {
            type: 'number',
            isRequired: true,
        },
        signed_hash: {
            type: 'string',
            description: `SHA-256 hash of the signed document`,
            isRequired: true,
        },
        timestamp: {
            type: 'string',
            description: `The time when the document was signed`,
            isRequired: true,
            format: 'date-time',
        },
        certified_timestamp: {
            type: 'any-of',
            description: `Certified timestamp if available`,
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        ip_address: {
            type: 'any-of',
            description: `IP address of the signer`,
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        id: {
            type: 'number',
            isRequired: true,
        },
    },
} as const;
