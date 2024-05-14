export const $DocumentRead = {
    properties: {
        id: {
            type: "number",
            isRequired: true,
        },
        title: {
            type: "string",
            isRequired: true,
        },
        file: {
            type: "string",
            isRequired: true,
        },
        file_url: {
            type: "string",
            isRequired: false,
        },
        status: {
            type: "string",
            isRequired: true,
        },
        created_at: {
            type: "string",
            isRequired: true,
        },
        updated_at: {
            type: "string",
            isRequired: true,
        },
        owner: {
            properties: {
                email: {
                    type: "string",
                    isRequired: true,
                },
                is_active: {
                    type: "boolean",
                    isRequired: true,
                },
                is_superuser: {
                    type: "boolean",
                    isRequired: true,
                },
                id: {
                    type: "number",
                    isRequired: true,
                },
                full_name: {
                    type: "string",
                    isRequired: true,
                },
                created_at: {
                    type: "string",
                    isRequired: true,
                },
                updated_at: {
                    type: "string",
                    isRequired: true,
                },
            },
            isRequired: true,
        },
        doc_requests: {
            type: "array",
            contains: {
                properties: {
                    name: {
                        type: "string",
                        isRequired: true,
                    },
                    delivery_mode: {
                        type: "string",
                        isRequired: true,
                    },
                    ordered_signers: {
                        type: "boolean",
                        isRequired: true,
                    },
                    reminder_settings: {
                        properties: {
                            interval_in_days: {
                                type: "number",
                                isRequired: true,
                            },
                            max_occurrences: {
                                type: "number",
                                isRequired: true,
                            },
                            timezone: {
                                type: "string",
                                isRequired: true,
                            },
                        },
                        isRequired: true,
                    },
                    expiration_date: {
                        type: "string",
                        isRequired: true,
                    },
                    message: {
                        type: "string",
                        isRequired: true,
                    },
                    expiry_date: {
                        type: "string",
                        isRequired: true,
                    },
                    id: {
                        type: "number",
                        isRequired: true,
                    },
                    sender_id: {
                        type: "number",
                        isRequired: true,
                    },
                    created_at: {
                        type: "string",
                        isRequired: true,
                    },
                    updated_at: {
                        type: "string",
                        isRequired: true,
                    },
                },
            },
            isRequired: true,
        },
        signature_fields: {
            type: "array",
            contains: {
                properties: {
                    type: {
                        type: "string",
                        isRequired: true,
                    },
                    page: {
                        type: "number",
                        isRequired: true,
                    },
                    id: {
                        type: "number",
                        isRequired: true,
                    },
                    signer_id: {
                        type: "number",
                        isRequired: true,
                    },
                    document_id: {
                        type: "number",
                        isRequired: true,
                    },
                    signature_request_id: {
                        type: "number",
                        isRequired: true,
                    },
                    created_at: {
                        type: "string",
                        isRequired: true,
                    },
                    updated_at: {
                        type: "string",
                        isRequired: true,
                    },
                    radios: {
                        type: "array",
                        contains: {
                            properties: {
                                name: {
                                    type: "string",
                                    isRequired: true,
                                },
                                x: {
                                    type: "number",
                                    isRequired: true,
                                },
                                y: {
                                    type: "number",
                                    isRequired: true,
                                },
                                size: {
                                    type: "number",
                                    isRequired: true,
                                },
                            },
                        },
                        isRequired: true,
                    },
                },
            },
            isRequired: true,
        },
    },
} as const;
