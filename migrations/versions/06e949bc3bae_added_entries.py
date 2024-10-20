"""added Entries

Revision ID: 06e949bc3bae
Revises: 3e30e291ad2c
Create Date: 2024-10-16 16:03:19.706312

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '06e949bc3bae'
down_revision = '3e30e291ad2c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('profile_pic',
               existing_type=sa.BLOB(),
               type_=sa.String(length=300),
               existing_nullable=True)
        batch_op.alter_column('member_since',
               existing_type=sa.DATE(),
               type_=sa.DateTime(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('member_since',
               existing_type=sa.DateTime(),
               type_=sa.DATE(),
               existing_nullable=True)
        batch_op.alter_column('profile_pic',
               existing_type=sa.String(length=300),
               type_=sa.BLOB(),
               existing_nullable=True)

    # ### end Alembic commands ###
