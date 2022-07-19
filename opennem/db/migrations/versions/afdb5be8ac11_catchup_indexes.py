# pylint: disable=no-member
"""
Catchup indexes

Revision ID: afdb5be8ac11
Revises: 2999c8b2978f
Create Date: 2021-03-18 06:50:56.174087

"""
from alembic import op

# revision identifiers, used by Alembic.
revision = "afdb5be8ac11"
down_revision = "2999c8b2978f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.drop_index("ix_facility_code", table_name="facility")
    op.create_index(op.f("ix_facility_code"), "facility", ["code"], unique=True)

    op.drop_constraint("fk_facility_station_code", "facility", type_="foreignkey")
    op.create_foreign_key(
        "fk_facility_station_code",
        "facility",
        "station",
        ["station_id"],
        ["id"],
    )
    op.drop_index("ix_station_code", table_name="station")
    op.create_index(op.f("ix_station_code"), "station", ["code"], unique=True)


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_station_code"), table_name="station")
    op.create_index("ix_station_code", "station", ["code"], unique=False)
    op.drop_constraint("fk_facility_station_code", "facility", type_="foreignkey")
    op.create_foreign_key(
        "fk_facility_station_code",
        "facility",
        "station",
        ["station_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.drop_index(op.f("ix_facility_code"), table_name="facility")
    op.create_index("ix_facility_code", "facility", ["code"], unique=False)
    # ### end Alembic commands ###
