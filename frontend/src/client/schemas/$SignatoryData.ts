/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $SignatoryData = {
    properties: {
        info: {
            type: 'SignatoryBase',
            isRequired: true,
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
