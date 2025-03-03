"""Creation table

Revision ID: a359a29e7732
Revises: 
Create Date: 2024-04-11 06:50:22.076280

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'a359a29e7732'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('banner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('feature_id', sa.Integer(), nullable=True),
    sa.Column('tag_ids', postgresql.ARRAY(sa.Integer()), nullable=True),
    sa.Column('title', sa.String(length=500), nullable=True),
    sa.Column('text', sa.String(length=5000), nullable=True),
    sa.Column('url', sa.String(length=500), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
    sa.Column('updated_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('banner_tags_features',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('banner_id', sa.Integer(), nullable=True),
    sa.Column('feature_id', sa.Integer(), nullable=True),
    sa.Column('tag_ids', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['banner_id'], ['banner.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('banner_tags_features')
    op.drop_table('banner')
    # ### end Alembic commands ###
