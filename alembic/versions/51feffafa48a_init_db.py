"""Init DB

Revision ID: 51feffafa48a
Revises: 
Create Date: 2022-05-16 19:36:58.051495

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = '51feffafa48a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create extensions
    op.execute(sa.text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('aktivnost',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
    sa.Column('naziv', sa.String(), nullable=True),
    sa.Column('opis', sa.String(), nullable=True),
    sa.Column('pocetak', sa.DateTime(), nullable=True),
    sa.Column('kraj', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('sudionik',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sqlalchemy_utils.types.uuid.UUIDType(), nullable=True),
    sa.Column('ime', sa.String(), nullable=True),
    sa.Column('prezime', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('tel', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('aktivnost_sudionika',
    sa.Column('sudionik_id', sa.Integer(), nullable=False),
    sa.Column('aktivnost_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['aktivnost_id'], ['aktivnost.id'], ),
    sa.ForeignKeyConstraint(['sudionik_id'], ['sudionik.id'], ),
    sa.PrimaryKeyConstraint('sudionik_id', 'aktivnost_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('aktivnost_sudionika')
    op.drop_table('sudionik')
    op.drop_table('aktivnost')
    # ### end Alembic commands ###
    # Drop extensions
    op.execute(sa.text("DROP EXTENSION IF EXISTS pg_trgm;"))
