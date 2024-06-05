/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserUpdateMe = {
    properties: {
        email: {
            type: 'any-of',
            description: `User email`,
            contains: [{
                type: 'string',
                format: 'email',
            }, {
                type: 'null',
            }],
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
            type: 'any-of',
            description: `User's first name`,
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        last_name: {
            type: 'any-of',
            description: `User's last name`,
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
    },
} as const;
