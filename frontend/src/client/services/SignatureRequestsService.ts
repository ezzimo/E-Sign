import { OpenAPI } from "../core/OpenAPI";
import { request } from "../core/request";
import { SignatureRequestCreate } from "../models/SignatureRequestCreate";
import { SignatureRequestRead } from "../models/SignatureRequestRead";

export const initiateSignatureRequest = (
  data: SignatureRequestCreate,
): Promise<SignatureRequestRead> => {
  return request<SignatureRequestRead>(OpenAPI, {
    method: "POST",
    url: "/api/v1/signature_requests/",
    body: data,
    mediaType: "application/json",
  });
};

export const fetchSignatureRequests = (): Promise<SignatureRequestRead[]> => {
  return request<SignatureRequestRead[]>(OpenAPI, {
    method: "GET",
    url: "/api/v1/signature_requests/",
  });
};
