/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */

import type { FieldCreate } from './FieldCreate';

export type SignatoryCreate = {
    /**
     * First name of the signatory
     */
    first_name: string;
    /**
     * Last name of the signatory
     */
    last_name: string;
    /**
     * Email of the signatory
     */
    email: string;
    /**
     * Phone number in E.164 format
     */
    phone_number: string;
    /**
     * Order in which the signatory signs
     */
    signing_order: number;
    /**
     * Role of the signatory
     */
    role: string;
    /**
     * Fields for this signatory
     */
    fields: Array<FieldCreate>;
};

