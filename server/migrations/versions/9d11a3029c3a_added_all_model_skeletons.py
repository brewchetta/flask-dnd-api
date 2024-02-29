"""added all model skeletons

Revision ID: 9d11a3029c3a
Revises: 73229d57db43
Create Date: 2024-02-29 16:08:40.490860

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d11a3029c3a'
down_revision = '73229d57db43'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('actions_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('condition_immunities_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('damage_immunities_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('damage_resistances_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('damage_vulnerabilities_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('languages_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('monster_spells_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('senses_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('special_abilities_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('spells_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('spells_table')
    op.drop_table('special_abilities_table')
    op.drop_table('senses_table')
    op.drop_table('monster_spells_table')
    op.drop_table('languages_table')
    op.drop_table('damage_vulnerabilities_table')
    op.drop_table('damage_resistances_table')
    op.drop_table('damage_immunities_table')
    op.drop_table('condition_immunities_table')
    op.drop_table('actions_table')
    # ### end Alembic commands ###
