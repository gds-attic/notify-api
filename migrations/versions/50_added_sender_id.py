"""empty message

Revision ID: 50_added_sender_id
Revises: 40_sent_at_column
Create Date: 2015-10-19 15:32:00.951750

"""

# revision identifiers, used by Alembic.
revision = '50_added_sender_id'
down_revision = '40_sent_at_column'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('notifications', sa.Column('sender_id', sa.String(length=255), nullable=True))
    op.create_index(op.f('ix_notifications_sender_id'), 'notifications', ['sender_id'], unique=False)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_notifications_sender_id'), table_name='notifications')
    op.drop_column('notifications', 'sender_id')
    ### end Alembic commands ###