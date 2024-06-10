/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $RadioCreate = {
    properties: {
        name: {
            type: 'string',
            isRequired: true,
        },
        'x': {
            type: 'number',
            isRequired: true,
        },
        'y': {
            type: 'number',
            isRequired: true,
        },
        size: {
            type: 'any-of',
            contains: [{
                type: 'number',
            }, {
                type: 'null',
            }],
        },
    },
} as const;
