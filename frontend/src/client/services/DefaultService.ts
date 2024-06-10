/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';

export class DefaultService {

    /**
     * Root
     * @returns any Successful Response
     * @throws ApiError
     */
    public static defaultRoot(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/',
        });
    }

    /**
     * Test Static
     * @returns any Successful Response
     * @throws ApiError
     */
    public static defaultTestStatic(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/test-static',
        });
    }

}
