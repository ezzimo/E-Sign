/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $SignatureRequestCreate = {
    properties: {
        name: {
            type: 'string',
            isRequired: true,
        },
        delivery_mode: {
            type: 'string',
            isRequired: true,
        },
        ordered_signers: {
            type: 'boolean',
            isRequired: true,
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
            type: 'array',
            contains: {
                type: 'SignatoryData',
            },
            isRequired: true,
        },
        documents: {
            type: 'array',
            contains: {
                type: 'number',
            },
            isRequired: true,
        },
    },
} as const;
