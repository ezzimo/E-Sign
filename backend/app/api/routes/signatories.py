from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import get_db
from app.crud import signatory_crud
from app.models.signatory_model import Signatory
from app.schemas.signatory_schema import SignatoryCreate, SignatoryOut, SignatoryUpdate

router = APIRouter()


@router.post("/", response_model=SignatoryOut)
def create_signatory(signatory: SignatoryCreate, db: Session = Depends(get_db)):
    return signatory_crud.create_signatory(db=db, obj_in=signatory)


@router.get("/{signatory_id}", response_model=SignatoryOut)
def read_signatory(signatory_id: int, db: Session = Depends(get_db)):
    db_signatory = signatory_crud.get_signatory(db=db, signatory_id=signatory_id)
    if db_signatory is None:
        raise HTTPException(status_code=404, detail="Signatory not found")
    return db_signatory


@router.get("/document/{document_id}", response_model=list[SignatoryOut])
def read_signatories_by_document(document_id: int, db: Session = Depends(get_db)):
    db_signatories = signatory_crud.get_signatories_by_document(
        db=db, document_id=document_id
    )
    if not db_signatories:
        raise HTTPException(
            status_code=404, detail="No signatories found for this document"
        )
    return db_signatories


@router.put("/{signatory_id}", response_model=SignatoryOut)
def update_signatory(
    signatory_id: int, signatory: SignatoryUpdate, db: Session = Depends(get_db)
):
    db_signatory = signatory_crud.get_signatory(db=db, signatory_id=signatory_id)
    if db_signatory is None:
        raise HTTPException(status_code=404, detail="Signatory not found")
    return signatory_crud.update_signatory(db=db, db_obj=db_signatory, obj_in=signatory)


@router.delete("/{signatory_id}", response_model=dict)
def delete_signatory(signatory_id: int, db: Session = Depends(get_db)):
    signatory_crud.delete_signatory(db=db, signatory_id=signatory_id)
    return {"ok": True}


@router.patch("/signatories/{signatory_id}/link-user/")
def link_signatory_to_user(
    signatory_id: int, user_id: int, db: Session = Depends(get_db)
):
    signatory = db.get(Signatory, signatory_id)
    if not signatory:
        raise HTTPException(status_code=404, detail="Signatory not found")
    signatory.signer_id = user_id
    db.commit()
    return signatory
