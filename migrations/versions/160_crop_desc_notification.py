"""empty message

Revision ID: 160_crop_desc_notification
Revises: 150_add_filename_to_job
Create Date: 2015-10-30 15:05:11.943803

"""

# revision identifiers, used by Alembic.
revision = '160_crop_desc_notification'
down_revision = '150_add_filename_to_job'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('notifications', 'description')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notifications', sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    ### end Alembic commands ###
