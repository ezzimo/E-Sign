import logging
from pathlib import Path

from sqlmodel import select

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.api.deps import SessionDep
from app.models.models import Document
from app.services.file_service import verify_secure_link_token

logger = logging.getLogger(__name__)
router = APIRouter()

# Define the base directory for the static files
STATIC_FILES_DIR = Path("/app/static/document_files")


@router.get("/sign_document", response_class=JSONResponse)
def access_document_with_token(*, session: SessionDep, token: str = Query(...)) -> JSONResponse:
    payload = verify_secure_link_token(token)
    if payload is None:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    document_id = payload.get("document_id")
    email = payload.get("sub")
    logger.info(f"The document id is: {document_id}")
    logger.info(f"The email is: {email}")
    if document_id is None or email is None:
        raise HTTPException(status_code=400, detail="Invalid token payload")

    document_statement = select(Document).where(Document.id == int(document_id))
    document = session.exec(document_statement).first()
    if document is None:
        raise HTTPException(status_code=404, detail="Document not found")

    file_path = STATIC_FILES_DIR / f"{document.owner_id}_{document.file}"
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    document_url = f"/static/document_files/{document.owner_id}_{document.file}"
    return JSONResponse(content={"document_url": document_url})
