"""Field model update 2

Revision ID: d19d0295411a
Revises: 06f9e7ed8c97
Create Date: 2024-04-30 10:23:24.103573

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = 'd19d0295411a'
down_revision = '06f9e7ed8c97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('docfield', 'x',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('docfield', 'y',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('docfield', 'height',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('docfield', 'width',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('docfield', 'width',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('docfield', 'height',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('docfield', 'y',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('docfield', 'x',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###