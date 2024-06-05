/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $SignatureRequestUpdate = {
    properties: {
        name: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        delivery_mode: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        ordered_signers: {
            type: 'any-of',
            contains: [{
                type: 'boolean',
            }, {
                type: 'null',
            }],
        },
        reminder_settings: {
            type: 'any-of',
            contains: [{
                type: 'ReminderSettingsSchema',
            }, {
                type: 'null',
            }],
        },
        expiry_date: {
            type: 'any-of',
            contains: [{
                type: 'string',
                format: 'date-time',
            }, {
                type: 'null',
            }],
        },
        message: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        signatories: {
            type: 'any-of',
            contains: [{
                type: 'array',
                contains: {
                    type: 'SignatoryData',
                },
            }, {
                type: 'null',
            }],
        },
        documents: {
            type: 'any-of',
            contains: [{
                type: 'array',
                contains: {
                    type: 'number',
                },
            }, {
                type: 'null',
            }],
        },
    },
} as const;
