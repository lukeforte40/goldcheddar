"""init v.1

Revision ID: 618fe7fd6076
Revises: 
Create Date: 2020-09-03 03:14:37.120314

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '618fe7fd6076'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('pub_date', sa.DateTime(), nullable=False),
    sa.Column('author', sa.String(length=80), nullable=True),
    sa.Column('banner', sa.String(length=40), nullable=True),
    sa.Column('description', sa.String(length=256), nullable=True),
    sa.Column('content', sa.Text(length=4294000000), nullable=True),
    sa.Column('category', sa.String(length=100), nullable=True),
    sa.Column('read_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('name', sa.String(length=25), nullable=False),
    sa.PrimaryKeyConstraint('name'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=50), nullable=True),
    sa.Column('passwordH', sa.String(length=128), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('post_tags',
    sa.Column('tag', sa.String(length=25), nullable=False),
    sa.Column('post', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['tag'], ['tag.name'], ),
    sa.PrimaryKeyConstraint('tag')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('post_tags')
    op.drop_table('user')
    op.drop_table('tag')
    op.drop_table('posts')
    # ### end Alembic commands ###