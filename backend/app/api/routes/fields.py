from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.api.deps import get_db
from app.crud.field_crud import create_field, delete_field, get_field, update_field
from app.schemas.schemas import FieldCreate, FieldOut, FieldUpdate

router = APIRouter()


@router.post(
    "/{signature_request_id}/documents/{document_id}/fields",
    response_model=FieldOut,
)
def create_field_endpoint(
    field: FieldCreate,
    signature_request_id: int,
    document_id: int,
    db: Session = Depends(get_db),
):
    return create_field(
        db,
        field_data=field,
        signature_request_id=signature_request_id,
        document_id=document_id,
    )


@router.get("/{field_id}", response_model=FieldOut)
def read_field(field_id: int, db: Session = Depends(get_db)):
    field = get_field(db, field_id)

    if not field:
        raise HTTPException(status_code=404, detail="Field not found")

    return field


@router.put("/{field_id}", response_model=FieldOut)
def update_field_endpoint(
    field_id: int, field: FieldUpdate, db: Session = Depends(get_db)
):
    return update_field(db, field_id=field_id, field_data=field)


@router.delete("/{field_id}")
def delete_field_endpoint(field_id: int, db: Session = Depends(get_db)):
    delete_field(db, field_id)
    return {"ok": True}
