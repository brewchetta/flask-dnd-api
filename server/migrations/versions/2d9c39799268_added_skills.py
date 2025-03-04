"""added skills

Revision ID: 2d9c39799268
Revises: 7b8a0c295f5f
Create Date: 2024-02-28 16:31:24.179598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d9c39799268'
down_revision = '7b8a0c295f5f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('skills_table',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('monster_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['monster_id'], ['monsters_table.id'], name=op.f('fk_skills_table_monster_id_monsters_table')),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('skills_table')
    # ### end Alembic commands ###
