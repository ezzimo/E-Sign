import logging

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class MIMETypeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        logger.debug(f"Request path: {request.url.path}")
        response = await call_next(request)
        if request.url.path.endswith(".pdf"):
            response.headers["Content-Type"] = "application/pdf"
        elif request.url.path.endswith(".jpg") or request.url.path.endswith(".jpeg"):
            response.headers["Content-Type"] = "image/jpeg"
        elif request.url.path.endswith(".png"):
            response.headers["Content-Type"] = "image/png"
        elif request.url.path.endswith(".gif"):
            response.headers["Content-Type"] = "image/gif"
        logger.debug(f"Response headers: {response.headers}")
        return response
