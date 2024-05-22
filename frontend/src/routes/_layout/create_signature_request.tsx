import { createRoute } from "@tanstack/react-router";
import CreateSignatureRequestForm from "../../components/SignatureRequests/CreateSignatureRequestForm";
import { Route as LayoutRoute } from "../_layout";

export const Route = createRoute({
  getParentRoute: () => LayoutRoute,
  path: "/new_signature_requests",
  component: CreateSignatureRequestForm,
});
