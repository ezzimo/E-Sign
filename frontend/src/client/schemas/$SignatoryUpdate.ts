/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $SignatoryUpdate = {
    properties: {
        first_name: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        last_name: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        email: {
            type: 'any-of',
            contains: [{
                type: 'string',
                format: 'email',
            }, {
                type: 'null',
            }],
        },
        phone_number: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        signing_order: {
            type: 'any-of',
            contains: [{
                type: 'number',
            }, {
                type: 'null',
            }],
        },
        role: {
            type: 'string',
            description: `Role of the signatory`,
            isRequired: true,
        },
        signature_image: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        signed_at: {
            type: 'any-of',
            contains: [{
                type: 'string',
                format: 'date-time',
            }, {
                type: 'null',
            }],
        },
    },
} as const;
