/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ReminderSettingsSchema = {
    properties: {
        interval_in_days: {
            type: 'number',
            isRequired: true,
        },
        max_occurrences: {
            type: 'number',
            isRequired: true,
        },
        timezone: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
    },
} as const;
