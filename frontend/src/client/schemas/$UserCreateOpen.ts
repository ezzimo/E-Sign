/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserCreateOpen = {
    properties: {
        email: {
            type: 'string',
            description: `User email`,
            isRequired: true,
            format: 'email',
        },
        password: {
            type: 'string',
            description: `User's password`,
            isRequired: true,
            minLength: 8,
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
        company: {
            type: 'any-of',
            description: `User's company`,
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
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
