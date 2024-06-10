/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $Body_documents_update_document = {
    properties: {
        title: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        status: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        new_file: {
            type: 'any-of',
            contains: [{
                type: 'binary',
                format: 'binary',
            }, {
                type: 'null',
            }],
        },
    },
} as const;
