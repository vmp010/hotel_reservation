"""remove user_id from hotel_rooms

Revision ID: de534b1241c4
Revises: 44b29ae8ee2b
Create Date: 2025-11-14 03:51:42.175315

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'de534b1241c4'
down_revision: Union[str, Sequence[str], None] = '44b29ae8ee2b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # 1. 刪除 hotel_rooms.user_id
    op.drop_column('hotel_rooms', 'user_id')
    
    # 2. 新增 hotel_rooms.owner（如果不存在）
    # 先檢查是否已存在（避免重複執行報錯）
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = {col['name'] for col in inspector.get_columns('hotel_rooms')}
    
    if 'owner' not in columns:
        op.add_column('hotel_rooms', sa.Column('owner', sa.Integer(), nullable=True))
        op.create_foreign_key('fk_hotel_owner', 'hotel_rooms', 'owners', ['owner'], ['id'], ondelete='CASCADE')
    
    # 3. 刪除 users.hotel_id（如果存在）
    user_columns = {col['name'] for col in inspector.get_columns('users')}
    if 'hotel_id' in user_columns:
        op.drop_column('users', 'hotel_id')



def downgrade() -> None:
    # 回退時重新加上欄位（視需求決定是否實作）
    op.add_column('hotel_rooms', sa.Column('user_id', mysql.INTEGER(), nullable=True))
    op.add_column('users', sa.Column('hotel_id', mysql.INTEGER(), nullable=True))
    op.drop_constraint('fk_hotel_owner', 'hotel_rooms', type_='foreignkey')
    op.drop_column('hotel_rooms', 'owner')
