import logging
import random
from pathlib import Path

from sqlmodel import select

from fastapi import APIRouter, HTTPException, Query, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.api.deps import SessionDep
from app.models.models import Document, Signatory
from app.services.file_service import (
    verify_secure_link_token,
    send_otp_code,
)

templates = Jinja2Templates(directory="signature-templates")
logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory store for OTPs
otp_store = {}
# Define the base directory for the static files
STATIC_FILES_DIR = Path("/app/static/document_files")


@router.get("/sign_document", response_class=HTMLResponse)
def access_document_with_token(*, session: SessionDep, token: str = Query(...), request: Request):
    payload = verify_secure_link_token(token)
    if payload is None:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

    document_ids = payload.get("document_ids")
    email = payload.get("sub")
    signatory_id = payload.get("signatory_id")
    if document_ids is None:
        raise HTTPException(status_code=400, detail="No document id in the payload")
    if email is None:
        raise HTTPException(status_code=400, detail="No email in the payload")
    if signatory_id is None:
        raise HTTPException(status_code=400, detail="No signatory id in the payload")

    document_urls = []
    for document_id in document_ids:
        document_statement = select(Document).where(Document.id == int(document_id))
        document = session.exec(document_statement).first()
        if document is None:
            raise HTTPException(
                status_code=404,
                detail="No Document corresponding to the payload document id",
            )
        file_path = STATIC_FILES_DIR / f"{document.owner_id}_{document.file}"
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")
        document_urls.append(f"document_files/{document.owner_id}_{document.file}")

    signatory_statement = select(Signatory).where(Signatory.id == int(signatory_id))
    signatory = session.exec(signatory_statement).first()

    return templates.TemplateResponse(
        "main_pages/signature.html", {
            "request": request,
            "document_urls": document_urls,
            "first_name": signatory.first_name,
            "last_name": signatory.last_name,
            "email": signatory.email,
            "phone_number": signatory.phone_number,
        }
    )


@router.post("/send_otp", response_class=JSONResponse)
def send_otp(email: str = Form(...)):
    otp = random.randint(100000, 999999)
    otp_store[email] = otp
    if not send_otp_code(email, otp):
        raise HTTPException(status_code=500, detail="Failed to send OTP")
    return JSONResponse(content={"message": "OTP sent successfully"})


@router.post("/verify_otp", response_class=JSONResponse)
def verify_otp(email: str = Form(...), otp: int = Form(...)):
    if email not in otp_store or otp_store[email] != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    del otp_store[email]
    # Perform signing logic here
    return JSONResponse(content={"message": "OTP verified successfully"})
