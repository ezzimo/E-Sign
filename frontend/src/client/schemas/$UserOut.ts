/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserOut = {
    properties: {
        email: {
            type: 'string',
            description: `User email address`,
            isRequired: true,
            format: 'email',
        },
        is_active: {
            type: 'boolean',
            description: `Is user active?`,
        },
        is_superuser: {
            type: 'boolean',
            description: `Is user a superuser?`,
        },
        id: {
            type: 'number',
            description: `User's unique ID`,
            isRequired: true,
        },
        full_name: {
            type: 'any-of',
            description: `User's full name`,
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        created_at: {
            type: 'string',
            description: `Creation timestamp`,
            isRequired: true,
            format: 'date-time',
        },
        updated_at: {
            type: 'string',
            description: `Last update timestamp`,
            isRequired: true,
            format: 'date-time',
        },
    },
} as const;
