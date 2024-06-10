/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $SignatureRequestRead = {
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
        id: {
            type: 'number',
            isRequired: true,
        },
        status: {
            type: 'SignatureRequestStatus',
            isRequired: true,
        },
        sender_id: {
            type: 'number',
            isRequired: true,
        },
        created_at: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
        updated_at: {
            type: 'string',
            isRequired: true,
            format: 'date-time',
        },
        documents: {
            type: 'array',
            contains: {
                type: 'DocumentOut',
            },
            isRequired: true,
        },
        signatories: {
            type: 'array',
            contains: {
                type: 'SignatoryOut',
            },
            isRequired: true,
        },
    },
} as const;
