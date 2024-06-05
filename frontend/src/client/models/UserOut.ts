/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type UserOut = {
    /**
     * User email address
     */
    email: string;
    /**
     * Is user active?
     */
    is_active?: boolean;
    /**
     * Is user a superuser?
     */
    is_superuser?: boolean;
    /**
     * User's unique ID
     */
    id: number;
    /**
     * User's full name
     */
    full_name?: (string | null);
    /**
     * Creation timestamp
     */
    created_at: string;
    /**
     * Last update timestamp
     */
    updated_at: string;
};

