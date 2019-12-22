"""empty message

Revision ID: f9ef10a5caef
Revises: 9739efb7e89f
Create Date: 2019-12-22 15:33:38.701209

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f9ef10a5caef'
down_revision = '9739efb7e89f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post', sa.Column('image_file', sa.String(length=20), nullable=True))
    with op.batch_alter_table('user') as batch_op:
        batch_op.drop_column('notes')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('notes', sa.TEXT(), nullable=True))
    with op.batch_alter_table('post') as batch_op:
        batch_op.drop_column('image_file')
    op.add_column('comment', sa.Column('username', sa.VARCHAR(), nullable=True))
    # ### end Alembic commands ###