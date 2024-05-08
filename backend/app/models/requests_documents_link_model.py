from sqlmodel import Field, SQLModel


class RequestDocumentLink(SQLModel, table=True):
    signature_request_id: int | None = Field(
        default=None, foreign_key="signaturerequest.id", primary_key=True
    )
    document_id: int | None = Field(
        default=None, foreign_key="document.id", primary_key=True
    )
