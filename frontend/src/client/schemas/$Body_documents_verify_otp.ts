/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Body_documents_verify_otp = {
    properties: {
        email: {
            type: 'string',
            isRequired: true,
        },
        otp: {
            type: 'number',
            isRequired: true,
        },
        signature_request_id: {
            type: 'number',
            isRequired: true,
        },
    },
} as const;
