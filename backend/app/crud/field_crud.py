import logging

from fastapi import HTTPException
from sqlmodel import Session

from app.models.field_model import DocField, FieldType, Radio
from app.schemas.field_schema import FieldCreate, FieldUpdate

logger = logging.getLogger(__name__)


def create_field(
    db: Session, field_data: FieldCreate, signature_request_id: int, document_id: int
) -> DocField:
    logger.info(
        f"Creating a new field of type {field_data.type} for signature request {signature_request_id}"
    )

    # Validate the field data
    try:
        field_data.validate_fields()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Create the DocField explicitly
    db_field = DocField(
        type=field_data.type,
        page=field_data.page,
        signature_request_id=signature_request_id,
        document_id=document_id,
        signer_id=field_data.signer_id,
        optional=field_data.optional,
        checked=field_data.checked,
        mention=field_data.mention,
        name=field_data.name,
        max_length=field_data.max_length,
        question=field_data.question,
        instruction=field_data.instruction,
        text=field_data.text,
        # Only include coordinates if they are valid
        x=field_data.x if field_data.x else None,
        y=field_data.y if field_data.y else None,
        height=field_data.height if field_data.height else None,
        width=field_data.width if field_data.width else None,
    )

    db.add(db_field)
    db.commit()
    db.refresh(db_field)

    # Handle potential radios for the radio group field
    if field_data.type == FieldType.RADIO_GROUP and field_data.radios:
        for radio_data in field_data.radios:
            db_radio = Radio(
                field_id=db_field.id,
                name=radio_data.name,
                x=radio_data.x,
                y=radio_data.y,
                size=radio_data.size if radio_data.size else 24,
            )
            db.add(db_radio)

        db.commit()

    return db_field


def get_field(db: Session, field_id: int) -> DocField | None:
    logger.debug(f"Retrieving field with ID {field_id}")
    return db.get(DocField, field_id)


def update_field(db: Session, field_id: int, field_data: FieldUpdate) -> DocField:
    logger.info(f"Updating field with ID {field_id}")
    db_field = db.get(DocField, field_id)

    if not db_field:
        logger.error(f"Field with ID {field_id} not found")
        raise HTTPException(status_code=404, detail="Field not found")

    for var, value in field_data.model_dump(exclude_unset=True).items():
        setattr(db_field, var, value)

    db.commit()
    db.refresh(db_field)

    return db_field


def delete_field(db: Session, field_id: int):
    logger.info(f"Deleting field with ID {field_id}")

    db_field = db.get(DocField, field_id)

    if not db_field:
        logger.error(f"Field with ID {field_id} not found")
        raise HTTPException(status_code=404, detail="Field not found")

    db.delete(db_field)
    db.commit()
