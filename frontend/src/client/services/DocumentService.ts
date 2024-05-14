import type {
    DocumentCreate,
    DocumentRead,
    DocumentResponse,
    DocumentUpdate,
} from "../../client";
import { OpenAPI } from "../core/OpenAPI";
import { request } from "../core/request";

export class DocumentService {
    public static async fetchDocuments(): Promise<DocumentRead[]> {
        return request<DocumentRead[]>(OpenAPI, {
            method: "GET",
            url: "/api/v1/documents/",
        });
    }

    public static async createDocument(
        data: DocumentCreate,
    ): Promise<DocumentResponse> {
        const formData = new FormData();
        formData.append("title", data.title);
        formData.append("status", data.status);
        if (data.file) formData.append("file", data.file);

        return request<DocumentResponse>(OpenAPI, {
            method: "POST",
            url: "/api/v1/documents/",
            body: formData,
            mediaType: "multipart/form-data",
        });
    }

    public static async updateDocument(id: number, data: DocumentUpdate): Promise<DocumentResponse> {
        const formData = new FormData();
        if (data.title !== null && data.title !== undefined) {
            formData.append('title', data.title);
        }
        if (data.status !== null && data.status !== undefined) {
            formData.append('status', data.status);
        }
        if (data.file instanceof File) {
            // Ensure the file is handled as a form input
            formData.append('new_file', data.file);  // Use `new_file` as expected by the backend
        }

        return request<DocumentResponse>(OpenAPI, {
            method: 'PUT',
            url: `/api/v1/documents/${id}`,
            body: formData,
            mediaType: 'multipart/form-data',
        });
    }

    public static async deleteDocument(id: number): Promise<void> {
        return request<void>(OpenAPI, {
            method: "DELETE",
            url: `/api/v1/documents/${id}`,
        });
    }
}
