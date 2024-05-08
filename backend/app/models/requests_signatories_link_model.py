from sqlmodel import Field, SQLModel


class RequestSignatoryLink(SQLModel, table=True):
    signature_request_id: int | None = Field(
        default=None, foreign_key="signaturerequest.id", primary_key=True
    )
    signatory_id: int | None = Field(
        default=None, foreign_key="signatory.id", primary_key=True
    )
