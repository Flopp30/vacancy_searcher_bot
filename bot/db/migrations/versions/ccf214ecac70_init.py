"""init

Revision ID: ccf214ecac70
Revises:
Create Date: 2023-05-03 21:20:04.378622
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ccf214ecac70'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
                    sa.Column('is_deleted', sa.Boolean(), nullable=True),
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('created_at', sa.DATE(), nullable=True),
                    sa.Column('updated_at', sa.DATE(), nullable=True),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    op.create_table('profiles',
                    sa.Column('firstname', sa.VARCHAR(length=32), nullable=True),
                    sa.Column('lastname', sa.VARCHAR(length=32), nullable=True),
                    sa.Column('professional_role', sa.VARCHAR(length=32), nullable=True),
                    sa.Column('grade', sa.Enum('trainee', 'junior', 'middle', 'senior', name='grade'), nullable=True),
                    sa.Column('work_type',
                              sa.Enum('Частичная занятость', 'Стажировка', 'Проектная работа', 'Полная занятость',
                                      name='work_types'), nullable=True),
                    sa.Column('region', sa.VARCHAR(length=32), nullable=True),
                    sa.Column('salary_from', sa.Integer(), nullable=True),
                    sa.Column('salary_to', sa.Integer(), nullable=True),
                    sa.Column('ready_for_relocation', sa.Boolean(), nullable=True),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('created_at', sa.DATE(), nullable=True),
                    sa.Column('updated_at', sa.DATE(), nullable=True),
                    sa.Column('is_deleted', sa.Boolean(), nullable=True),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profiles')
    op.drop_table('users')
    # ### end Alembic commands ###
