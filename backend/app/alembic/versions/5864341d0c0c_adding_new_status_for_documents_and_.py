"""Adding new status for Documents and SignatureRequest

Revision ID: 5864341d0c0c
Revises: 622d30b4f766
Create Date: 2024-06-25 10:59:12.991380

"""

import sqlalchemy as sa
import sqlmodel.sql.sqltypes
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "5864341d0c0c"
down_revision = "622d30b4f766"
branch_labels = None
depends_on = None

# Define the old and new ENUM options
old_document_options = ("DRAFT", "SENT_FOR_SIGNATURE", "VIEWED", "SIGNED", "REJECTED")
new_document_options = old_document_options + ("PARTIALLY_SIGNED",)

old_request_options = ("DRAFT", "SENT", "COMPLETED", "EXPIRED", "CANCELED")
new_request_options = old_request_options + ("PARTIALLY_SIGNED",)

# Define the ENUM types
old_document_type = postgresql.ENUM(*old_document_options, name="documentstatus")
new_document_type = postgresql.ENUM(*new_document_options, name="documentstatus")
tmp_document_type = sa.Enum(*new_document_options, name="tmp_documentstatus")

old_request_type = postgresql.ENUM(*old_request_options, name="signaturerequeststatus")
new_request_type = postgresql.ENUM(*new_request_options, name="signaturerequeststatus")
tmp_request_type = sa.Enum(*new_request_options, name="tmp_signaturerequeststatus")


def upgrade():
    # Create a temporary type for document status
    tmp_document_type.create(op.get_bind(), checkfirst=False)
    # Alter the document status column to use the temporary type
    op.alter_column(
        "document",
        "status",
        type_=tmp_document_type,
        postgresql_using="status::text::tmp_documentstatus",
    )
    # Drop the old document status type
    old_document_type.drop(op.get_bind(), checkfirst=False)
    # Create the new document status type
    new_document_type.create(op.get_bind(), checkfirst=False)
    # Alter the document status column to use the new type
    op.alter_column(
        "document",
        "status",
        type_=new_document_type,
        postgresql_using="status::text::documentstatus",
    )
    # Drop the temporary document status type
    tmp_document_type.drop(op.get_bind(), checkfirst=False)

    # Create a temporary type for signature request status
    tmp_request_type.create(op.get_bind(), checkfirst=False)
    # Alter the signature request status column to use the temporary type
    op.alter_column(
        "signaturerequest",
        "status",
        type_=tmp_request_type,
        postgresql_using="status::text::tmp_signaturerequeststatus",
    )
    # Drop the old signature request status type
    old_request_type.drop(op.get_bind(), checkfirst=False)
    # Create the new signature request status type
    new_request_type.create(op.get_bind(), checkfirst=False)
    # Alter the signature request status column to use the new type
    op.alter_column(
        "signaturerequest",
        "status",
        type_=new_request_type,
        postgresql_using="status::text::signaturerequeststatus",
    )
    # Drop the temporary signature request status type
    tmp_request_type.drop(op.get_bind(), checkfirst=False)


def downgrade():
    # Create a temporary type for document status
    tmp_document_type.create(op.get_bind(), checkfirst=False)
    # Alter the document status column to use the temporary type
    op.alter_column(
        "document",
        "status",
        type_=tmp_document_type,
        postgresql_using="status::text::tmp_documentstatus",
    )
    # Drop the new document status type
    new_document_type.drop(op.get_bind(), checkfirst=False)
    # Create the old document status type
    old_document_type.create(op.get_bind(), checkfirst=False)
    # Alter the document status column to use the old type
    op.alter_column(
        "document",
        "status",
        type_=old_document_type,
        postgresql_using="status::text::documentstatus",
    )
    # Drop the temporary document status type
    tmp_document_type.drop(op.get_bind(), checkfirst=False)

    # Create a temporary type for signature request status
    tmp_request_type.create(op.get_bind(), checkfirst=False)
    # Alter the signature request status column to use the temporary type
    op.alter_column(
        "signaturerequest",
        "status",
        type_=tmp_request_type,
        postgresql_using="status::text::tmp_signaturerequeststatus",
    )
    # Drop the new signature request status type
    new_request_type.drop(op.get_bind(), checkfirst=False)
    # Create the old signature request status type
    old_request_type.create(op.get_bind(), checkfirst=False)
    # Alter the signature request status column to use the old type
    op.alter_column(
        "signaturerequest",
        "status",
        type_=old_request_type,
        postgresql_using="status::text::signaturerequeststatus",
    )
    # Drop the temporary signature request status type
