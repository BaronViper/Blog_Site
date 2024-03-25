"""Initial migration.

Revision ID: 2af0f3fe0569
Revises: 
Create Date: 2023-05-23 10:36:08.674333

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2af0f3fe0569'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subject', schema=None) as batch_op:
        batch_op.alter_column('birth',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=250),
               existing_nullable=False)
        batch_op.alter_column('death',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=250),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('subject', schema=None) as batch_op:
        batch_op.alter_column('death',
               existing_type=sa.String(length=250),
               type_=sa.INTEGER(),
               existing_nullable=False)
        batch_op.alter_column('birth',
               existing_type=sa.String(length=250),
               type_=sa.INTEGER(),
               existing_nullable=False)

    # ### end Alembic commands ###