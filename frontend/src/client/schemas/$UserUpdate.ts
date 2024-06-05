/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserUpdate = {
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
        full_name: {
            type: 'any-of',
            description: `User's full name`,
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
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
