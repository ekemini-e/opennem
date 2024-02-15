# pylint: disable=no-member
"""
interval is part of primary key on milestones

Revision ID: 9b7c579cf297
Revises: 1485ce197dbd
Create Date: 2024-02-15 11:07:59.559537

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2


# revision identifiers, used by Alembic.
revision = "9b7c579cf297"
down_revision = "1485ce197dbd"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("alter table milestones drop constraint milestones_pkey")
    op.create_primary_key(
        "milestones_pkey",
        "milestones",
        ["record_id", "interval"],
    )


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###