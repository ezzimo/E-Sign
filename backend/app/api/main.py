from fastapi import APIRouter

from app.api.routes import (
    documents,
    items,
    login,
    signatories,
    signature_requests,
    users,
    utils,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(
    signatories.router, prefix="/signatories", tags=["signatories"]
)
api_router.include_router(
    signature_requests.router, prefix="/signature_requests", tags=["signature_requests"]
)
