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
            isRequired: true,
        },
        file_url: {
            type: "string",
            isRequired: false,
        },
    },
} as const;
