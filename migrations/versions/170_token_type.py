"""empty message

Revision ID: 170_token_type
Revises: 160_crop_desc_notification
Create Date: 2015-11-02 12:28:50.867580

"""

# revision identifiers, used by Alembic.
revision = '170_token_type'
down_revision = '160_crop_desc_notification'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('token', sa.Column('type', sa.String(length=255), nullable=True))
    op.execute("UPDATE token SET type='client'")
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('token', 'type')
    ### end Alembic commands ###
