/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserCreate = {
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
        password: {
            type: 'string',
            description: `User's password`,
            isRequired: true,
            minLength: 8,
        },
        first_name: {
            type: 'string',
            description: `User's first name`,
            isRequired: true,
        },
        last_name: {
            type: 'string',
            description: `User's last name`,
            isRequired: true,
        },
        role: {
            type: 'any-of',
            description: `User's role`,
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
    },
} as const;
