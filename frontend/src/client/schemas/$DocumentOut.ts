/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $DocumentOut = {
    properties: {
        title: {
            type: 'string',
            description: `Title of the document`,
            isRequired: true,
        },
        file: {
            type: 'string',
            description: `File path or identifier`,
            isRequired: true,
        },
        file_url: {
            type: 'any-of',
            description: `URL to view the document`,
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        status: {
            type: 'all-of',
            description: `Current status of the document`,
            contains: [{
                type: 'DocumentStatus',
            }],
            isRequired: true,
        },
        id: {
            type: 'number',
            description: `Unique identifier for the document`,
            isRequired: true,
        },
        created_at: {
            type: 'string',
            description: `Timestamp when the document was created`,
            isRequired: true,
            format: 'date-time',
        },
        updated_at: {
            type: 'string',
            description: `Timestamp when the document was last updated`,
            isRequired: true,
            format: 'date-time',
        },
        owner: {
            type: 'all-of',
            description: `User information of the owner`,
            contains: [{
                type: 'UserOut',
            }],
            isRequired: true,
        },
        signature_details: {
            type: 'any-of',
            contains: [{
                type: 'DocumentSignatureDetailsOut',
            }, {
                type: 'null',
            }],
        },
    },
} as const;
