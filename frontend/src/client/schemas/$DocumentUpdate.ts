export const $DocumentUpdate = {
    properties: {
        title: {
            type: "string",
        },
        status: {
            type: "string",
        },
        file: {
            type: "File",
        },
        file_url: {
            type: "string",
        },
    },
} as const;
