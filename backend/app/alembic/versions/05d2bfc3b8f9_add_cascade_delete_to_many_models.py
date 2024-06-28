"""Add cascade delete to many models

Revision ID: 05d2bfc3b8f9
Revises: 5864341d0c0c
Create Date: 2024-06-27 15:29:55.808129

"""

import sqlalchemy as sa
import sqlmodel.sql.sqltypes

from alembic import op

# revision identifiers, used by Alembic.
revision = "05d2bfc3b8f9"
down_revision = "5864341d0c0c"
branch_labels = None
depends_on = None


def upgrade():
    # Drop the existing foreign key constraint
    op.drop_constraint(
        "fk_document_signature_details_document_id",
        "documentsignaturedetails",
        type_="foreignkey",
    )
    op.drop_constraint("fk_document_owner_id", "document", type_="foreignkey")
    op.drop_constraint("fk_signatory_creator_id", "signatory", type_="foreignkey")
    op.drop_constraint("fk_radio_field_id", "radio", type_="foreignkey")
    op.drop_constraint("fk_doc_field_signer_id", "doc_field", type_="foreignkey")
    op.drop_constraint(
        "fk_audit_log_signature_request_id", "auditlog", type_="foreignkey"
    )
    op.drop_constraint(
        "fk_reminder_settings_request_id", "remindersettings", type_="foreignkey"
    )

    # Create a new foreign key constraint with ON DELETE CASCADE
    op.create_foreign_key(
        None,
        "documentsignaturedetails",
        "document",
        ["document_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        None, "document", "owner", ["owner_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "signatory", "creator", ["creator_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "radio", "doc_field", ["field_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None, "doc_field", "signatory", ["signer_id"], ["id"], ondelete="CASCADE"
    )
    op.create_foreign_key(
        None,
        "audit_log",
        "signature_request",
        ["signature_request_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.create_foreign_key(
        None, "reminder_settings", "request", ["request_id"], ["id"], ondelete="CASCADE"
    )


def downgrade():
    # Drop the new foreign key constraint
    op.drop_constraint(None, "documentsignaturedetails", type_="foreignkey")
    op.drop_constraint(None, "document", type_="foreignkey")
    op.drop_constraint(None, "signatory", type_="foreignkey")
    op.drop_constraint(None, "radio", type_="foreignkey")
    op.drop_constraint(None, "doc_field", type_="foreignkey")
    op.drop_constraint(None, "audit_log", type_="foreignkey")
    op.drop_constraint(None, "reminder_settings", type_="foreignkey")

    # Recreate the original foreign key constraint without ON DELETE CASCADE
    op.create_foreign_key(
        "document_signature_details_document_id_fkey",
        "documentsignaturedetails",
        "document",
        ["document_id"],
        ["id"],
    )
    op.create_foreign_key(
        "document_owner_id_fkey", "document", "owner", ["owner_id"], ["id"]
    )
    op.create_foreign_key(
        "signatory_creator_id_fkey", "signatory", "creator", ["creator_id"], ["id"]
    )
    op.create_foreign_key(
        "radio_field_id_fkey", "radio", "doc_field", ["field_id"], ["id"]
    )
    op.create_foreign_key(
        "doc_field_signer_id_fkey", "docfield", "signatory", ["signer_id"], ["id"]
    )
    op.create_foreign_key(
        "audit_log_signature_request_id_fkey",
        "auditlog",
        "signature_request",
        ["signature_request_id"],
        ["id"],
    )
    op.create_foreign_key(
        "reminder_settings_request_id_fkey",
        "remindersettings",
        "request",
        ["request_id"],
        ["id"],
    )
