import { createRoute } from "@tanstack/react-router";
import SignatureRequestList from "../../components/SignatureRequests/SignatureRequestList";
import { Route as LayoutRoute } from "../_layout";

// Route for listing signature requests
export const Route = createRoute({
  getParentRoute: () => LayoutRoute,
  path: "/signature_requests",
  component: SignatureRequestList,
});
