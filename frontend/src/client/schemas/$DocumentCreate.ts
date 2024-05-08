/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export const $DocumentCreate = {
	properties: {
		title: {
			type: "string",
			isRequired: true,
		},
		status: {
			type: "string",
			isRequired: true,
		},
		file: {
			type: "File",
		},
	},
} as const;
