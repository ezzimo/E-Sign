export const $SignatureRequestCreateSchema = {
    type: "object",
    properties: {
        name: { type: "string" },
        delivery_mode: { type: "string" },
        ordered_signers: { type: "boolean" },
        reminder_settings: {
            type: "object",
            properties: {
                interval_in_days: { type: "number" },
                max_occurrences: { type: "number" },
                timezone: { type: "string" }
            },
            required: ["interval_in_days", "max_occurrences", "timezone"]
        },
        expiration_date: { type: "string", format: "date-time" },
        message: { type: "string" },
        expiry_date: { type: "string", format: "date-time" },
        signatories: {
            type: "array",
            items: {
                type: "object",
                properties: {
                    info: {
                        type: "object",
                        properties: {
                            first_name: { type: "string" },
                            last_name: { type: "string" },
                            email: { type: "string", format: "email" },
                            phone_number: { type: "string" },
                            signing_order: { type: "number" },
                            role: { type: "string" }
                        },
                        required: ["first_name", "last_name", "email", "phone_number", "signing_order", "role"]
                    },
                    fields: {
                        type: "array",
                        items: {
                            type: "object",
                            properties: {
                                type: { type: "string" },
                                page: { type: "number" },
                                signer_id: { type: "number" },
                                document_id: { type: "string" },
                                x: { type: "number" },
                                y: { type: "number" },
                                height: { type: "number" },
                                width: { type: "number" },
                                optional: { type: "boolean" },
                                mention: { type: "string" },
                                name: { type: "string" },
                                checked: { type: "boolean" },
                                max_length: { type: "number" },
                                question: { type: "string" },
                                instruction: { type: "string" },
                                text: { type: "string" },
                                radios: {
                                    type: "array",
                                    items: {
                                        type: "object",
                                        properties: {
                                            name: { type: "string" },
                                            x: { type: "number" },
                                            y: { type: "number" },
                                            size: { type: "number" }
                                        },
                                        required: ["name", "x", "y", "size"]
                                    }
                                }
                            },
                            required: ["type", "page", "signer_id", "document_id", "x", "y", "height", "width", "optional", "mention", "name", "checked", "max_length", "question", "instruction", "text", "radios"]
                        }
                    }
                },
                required: ["info", "fields"]
            }
        },
        documents: {
            type: "array",
            items: { type: "number" }
        }
    },
    required: ["name", "delivery_mode", "ordered_signers", "reminder_settings", "expiration_date", "message", "expiry_date", "signatories", "documents"]
};
