/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type UserUpdate = {
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
     * User's full name
     */
    full_name?: (string | null);
    /**
     * User's company
     */
    company?: (string | null);
    /**
     * User's role
     */
    role?: (string | null);
};

