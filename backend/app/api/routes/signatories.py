from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import get_current_user_id, get_db
from app.crud import signatory_crud
from app.schemas.schemas import SignatoryCreate, SignatoryOut, SignatoryUpdate

router = APIRouter()


@router.post("/", response_model=SignatoryOut, status_code=201)
def create_signatory(
    signatory: SignatoryCreate,
    db: Session = Depends(get_db),
    creator_id: int = Depends(get_current_user_id),
):
    """
    Create a new signatory with the specified user as the creator.
    Automatically attempts to link a signer by email.
    """
    return signatory_crud.create_signatory(
        db=db, obj_in=signatory, creator_id=creator_id
    )


@router.get("/{signatory_id}", response_model=SignatoryOut)
def read_signatory(signatory_id: int, db: Session = Depends(get_db)):
    """
    Read a signatory by its ID.
    """
    signatory = signatory_crud.get_signatory(db, signatory_id)
    if not signatory:
        raise HTTPException(status_code=404, detail="Signatory not found")
    return signatory


@router.get("/document/{document_id}", response_model=list[SignatoryOut])
def read_signatories_by_document(document_id: int, db: Session = Depends(get_db)):
    """
    Read signatories associated with a specific document.
    """
    signatories = signatory_crud.get_signatories_by_document(
        db=db, document_id=document_id
    )
    if not signatories:
        raise HTTPException(
            status_code=404, detail="No signatories found for this document"
        )
    return signatories


@router.patch("/{signatory_id}", response_model=SignatoryOut)
def update_signatory(
    signatory_id: int, update_data: SignatoryUpdate, db: Session = Depends(get_db)
):
    """
    Update a signatory's information.
    """
    signatory = signatory_crud.update_signatory(
        db=db, signatory_id=signatory_id, update_data=update_data
    )
    return signatory


@router.delete("/{signatory_id}", response_model=dict)
def delete_signatory(signatory_id: int, db: Session = Depends(get_db)):
    """
    Delete a signatory from the database.
    """
    signatory_crud.delete_signatory(db=db, signatory_id=signatory_id)
    return {"ok": True}
