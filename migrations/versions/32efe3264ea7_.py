"""empty message

Revision ID: 32efe3264ea7
Revises: 
Create Date: 2022-11-29 16:50:10.448488

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '32efe3264ea7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('addproduct', sa.Column('image_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'addproduct', 'image', ['image_id'], ['id'])
    op.drop_constraint('image_ibfk_1', 'image', type_='foreignkey')
    op.drop_column('image', 'addproduct_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('image', sa.Column('addproduct_id', mysql.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('image_ibfk_1', 'image', 'addproduct', ['addproduct_id'], ['id'])
    op.drop_constraint(None, 'addproduct', type_='foreignkey')
    op.drop_column('addproduct', 'image_id')
    # ### end Alembic commands ###
