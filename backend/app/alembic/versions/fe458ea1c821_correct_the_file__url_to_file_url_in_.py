"""correct the file__url to file_url in Document

Revision ID: fe458ea1c821
Revises: 47a8126a9204
Create Date: 2024-05-13 16:53:10.195220

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'fe458ea1c821'
down_revision = '47a8126a9204'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('file_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.drop_column('document', 'file__url')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('document', sa.Column('file__url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('document', 'file_url')
    # ### end Alembic commands ###