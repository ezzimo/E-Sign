/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

export type UserCreate = {
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
     * User's password
     */
    password: string;
    /**
     * User's first name
     */
    first_name: string;
    /**
     * User's last name
     */
    last_name: string;
    /**
     * User's role
     */
    role?: (string | null);
};

