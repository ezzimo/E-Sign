/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Body_documents_create_document = {
    properties: {
        title: {
            type: 'string',
            isRequired: true,
        },
        status: {
            type: 'string',
            isRequired: true,
        },
        file: {
            type: 'binary',
            isRequired: true,
            format: 'binary',
        },
    },
} as const;