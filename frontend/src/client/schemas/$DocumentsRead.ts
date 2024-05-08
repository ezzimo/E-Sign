/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import { $DocumentRead } from "./$DocumentRead";

export const $DocumentsRead = {
	properties: {
		documents: {
			type: "array",
			contains: $DocumentRead,
			isRequired: true,
		},
		count: {
			type: "number",
			isRequired: true,
		},
	},
} as const;
