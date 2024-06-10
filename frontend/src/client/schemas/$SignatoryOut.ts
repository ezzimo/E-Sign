/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $SignatoryOut = {
    properties: {
        first_name: {
            type: 'string',
            description: `First name of the signatory`,
            isRequired: true,
        },
        last_name: {
            type: 'string',
            description: `Last name of the signatory`,
            isRequired: true,
        },
        email: {
            type: 'string',
            description: `Email of the signatory`,
            isRequired: true,
            format: 'email',
        },
        phone_number: {
            type: 'string',
            description: `Phone number in E.164 format`,
            isRequired: true,
        },
        signing_order: {
            type: 'number',
            description: `Order in which the signatory signs`,
            isRequired: true,
        },
        role: {
            type: 'string',
            description: `Role of the signatory`,
            isRequired: true,
        },
        id: {
            type: 'number',
            description: `Unique ID of the signatory`,
            isRequired: true,
        },
        created_at: {
            type: 'string',
            description: `Creation time`,
            isRequired: true,
            format: 'date-time',
        },
        updated_at: {
            type: 'string',
            description: `Last update time`,
            isRequired: true,
            format: 'date-time',
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
        fields: {
            type: 'array',
            contains: {
                type: 'FieldCreate',
            },
            isRequired: true,
        },
    },
} as const;
