"""Add phone_number to Signatory

Revision ID: 841630e649fa
Revises: f5307fd3a309
Create Date: 2024-04-25 10:32:19.081381

"""
import sqlalchemy as sa
import sqlmodel.sql.sqltypes

from alembic import op

# revision identifiers, used by Alembic.
revision = '841630e649fa'
down_revision = 'f5307fd3a309'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('signatory', sa.Column('phone_number', sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('signatory', 'phone_number')
    # ### end Alembic commands ###