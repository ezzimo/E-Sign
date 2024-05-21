import { createRoute } from "@tanstack/react-router";
import CreateSignatureRequestWizard from "../../components/SignatureRequests/CreateSignatureRequestWizard";
import { Route as LayoutRoute } from "../_layout";

// Route for creating a new signature request
export const Route = createRoute({
  getParentRoute: () => LayoutRoute,
  path: "/new_signature_requests",
  component: CreateSignatureRequestWizard,
});
