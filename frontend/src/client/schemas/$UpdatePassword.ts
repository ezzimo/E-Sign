/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UpdatePassword = {
    properties: {
        current_password: {
            type: 'string',
            description: `Current password`,
            isRequired: true,
        },
        new_password: {
            type: 'string',
            description: `New password`,
            isRequired: true,
            minLength: 8,
        },
    },
} as const;
