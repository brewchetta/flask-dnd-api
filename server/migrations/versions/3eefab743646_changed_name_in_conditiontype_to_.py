"""changed name in ConditionType to condition_type

Revision ID: 3eefab743646
Revises: 515c3d7ff4a7
Create Date: 2024-03-01 10:16:40.393133

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3eefab743646'
down_revision = '515c3d7ff4a7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('condition_immunities_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('condition_type', sa.String(), nullable=False))
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('condition_immunities_table', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.VARCHAR(), nullable=False))
        batch_op.drop_column('condition_type')

    # ### end Alembic commands ###
