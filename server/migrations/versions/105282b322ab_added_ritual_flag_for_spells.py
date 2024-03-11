"""added ritual flag for spells

Revision ID: 105282b322ab
Revises: e939e8c6db36
Create Date: 2024-03-11 14:48:11.913067

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '105282b322ab'
down_revision = 'e939e8c6db36'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('spells_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('ritual', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('spells_table', schema=None) as batch_op:
        batch_op.drop_column('ritual')

    # ### end Alembic commands ###
