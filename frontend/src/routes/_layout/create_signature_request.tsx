import { createRoute } from '@tanstack/react-router';
import CreateSignatureRequest from '../../components/SignatureRequests';
import { Route as LayoutRoute } from "../_layout";

export const Route = createRoute({
  getParentRoute: () => LayoutRoute,
  path: "/new_signature_requests",
  component: CreateSignatureRequest,
});
