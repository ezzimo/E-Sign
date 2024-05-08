import logging
import sys

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import get_current_user, get_db
from app.crud.signature_request_crud import (
    create_signature_request,
    delete_signature_request,
    get_signatories_by_signature_request,
    get_signature_request,
    get_signature_requests_by_document,
    update_signature_request,
)
from app.models.user_model import User
from app.schemas.signatory_schema import SignatoryOut
from app.schemas.signature_request_schema import (
    SignatureRequestCreate,
    SignatureRequestRead,
    SignatureRequestUpdate,
)
from app.utils import send_signature_request_email

# Create a logger for your application
logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/", response_model=SignatureRequestRead, status_code=201)
def initiate_signature_request(
    signature_request: SignatureRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Initiate a new signature request.
    """
    signature_request_data = create_signature_request(
        db=db, request_data=signature_request, sender_id=current_user.id
    )

    # Send an email notification to all signatories
    for signatory in signature_request_data.signatories:
        send_signature_request_email(
            email_to=signatory.email,
            document_title="signature request",
            link="link_to_sign_document",
            message=signature_request_data.message,
        )

    return signature_request_data


@router.post("/create", response_model=SignatureRequestRead)
def create_request(
    signature_request: SignatureRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Create a new signature request.
    """
    request = create_signature_request(
        db=db, request=signature_request, sender_id=current_user.id
    )
    signatory_email = db.get(User, request.signatory_id).email
    send_signature_request_email(
        email_to=signatory_email,
        link="link_to_sign_document",
        message=request.message,
    )
    return request


@router.get("/{request_id}", response_model=SignatureRequestRead)
def read_request(request_id: int, db: Session = Depends(get_db)):
    """
    Get a signature request by ID.
    """
    db_request = get_signature_request(db=db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Signature request not found")
    return db_request


@router.get("/document/{document_id}", response_model=list[SignatureRequestRead])
def read_requests_by_document(document_id: int, db: Session = Depends(get_db)):
    """
    Get all signature requests for a specific document.
    """
    requests = get_signature_requests_by_document(db=db, document_id=document_id)
    return requests


@router.put("/{request_id}", response_model=SignatureRequestRead)
def update_request(
    request_id: int,
    signature_request: SignatureRequestUpdate,
    db: Session = Depends(get_db),
):
    """
    Update a signature request.
    """
    db_request = get_signature_request(db=db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Signature request not found")
    updated_request = update_signature_request(
        db=db, db_obj=db_request, obj_in=signature_request
    )
    return updated_request


@router.delete("/{request_id}", response_model=dict)
def delete_request(request_id: int, db: Session = Depends(get_db)):
    """
    Delete a signature request.
    """
    db_request = get_signature_request(db=db, request_id=request_id)
    if db_request is None:
        raise HTTPException(status_code=404, detail="Signature request not found")
    delete_signature_request(db=db, request_id=request_id)
    return {"message": "Signature request deleted successfully"}


@router.get(
    "/signature-request/{request_id}/signers", response_model=list[SignatoryOut]
)
def list_signature_request_signers(request_id: int, db: Session = Depends(get_db)):
    """
    List all signatories for a specific signature request.
    """
    signatories = get_signatories_by_signature_request(db, request_id)
    if not signatories:
        raise HTTPException(
            status_code=404, detail="No signatories found for this signature request."
        )
    return signatories
