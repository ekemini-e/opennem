# pylint: disable=no-member
"""
cleanup revisions

Revision ID: b207a3b6c080
Revises: 61b31447e61b
Create Date: 2024-08-03 12:36:39.622088

"""
from alembic import op
import sqlalchemy as sa
import geoalchemy2
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b207a3b6c080"
down_revision = "61b31447e61b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "at_network_flows_v3",
        sa.Column("trading_interval", postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column("network_id", sa.Text(), nullable=False),
        sa.Column("network_region", sa.Text(), nullable=False),
        sa.Column("energy_imports", sa.Numeric(), nullable=True),
        sa.Column("energy_exports", sa.Numeric(), nullable=True),
        sa.Column("market_value_imports", sa.Numeric(), nullable=True),
        sa.Column("market_value_exports", sa.Numeric(), nullable=True),
        sa.Column("emissions_imports", sa.Numeric(), nullable=True),
        sa.Column("emissions_exports", sa.Numeric(), nullable=True),
        sa.ForeignKeyConstraint(["network_id"], ["network.code"], name="fk_at_network_flows_network_code"),
        sa.PrimaryKeyConstraint("trading_interval", "network_id", "network_region"),
    )
    op.create_index(
        "idx_at_network_flows_v3_trading_interval_facility_code",
        "at_network_flows_v3",
        ["trading_interval", "network_id", "network_region"],
        unique=False,
    )
    op.create_index(
        "idx_at_network_flowsy_v3_network_id_trading_interval",
        "at_network_flows_v3",
        ["network_id", sa.text("trading_interval DESC")],
        unique=False,
    )
    op.create_index(op.f("ix_at_network_flows_v3_network_id"), "at_network_flows_v3", ["network_id"], unique=False)
    op.create_index(
        op.f("ix_at_network_flows_v3_network_region"), "at_network_flows_v3", ["network_region"], unique=False
    )
    op.create_index(
        op.f("ix_at_network_flows_v3_trading_interval"), "at_network_flows_v3", ["trading_interval"], unique=False
    )
    op.drop_constraint("fk_facility_station_code", "facility", type_="foreignkey")
    op.create_foreign_key("fk_facility_station_code", "facility", "station", ["station_id"], ["id"])
    op.create_index("idx_location_boundary", "location", ["boundary"], unique=False, postgresql_using="gist")
    op.add_column("milestones", sa.Column("network_region", sa.Text(), nullable=True))
    op.add_column("milestones", sa.Column("fueltech_group_id", sa.Text(), nullable=True))
    op.alter_column("milestones", "record_id", existing_type=sa.UUID(), type_=sa.Text(), existing_nullable=False)
    op.alter_column("milestones", "network_id", existing_type=sa.VARCHAR(), type_=sa.Text(), existing_nullable=True)
    op.alter_column("milestones", "fueltech_id", existing_type=sa.VARCHAR(), type_=sa.Text(), existing_nullable=True)
    op.create_foreign_key(None, "milestones", "fueltech_group", ["fueltech_group_id"], ["code"])
    op.drop_column("milestones", "facility_id")
    op.drop_index("ix_station_code", table_name="station")
    op.create_index(op.f("ix_station_code"), "station", ["code"], unique=True)
    op.drop_index("ix_stats_country_type", table_name="stats")
    op.drop_index("ix_stats_date", table_name="stats")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index("ix_stats_date", "stats", [sa.text("stat_date DESC")], unique=False)
    op.create_index("ix_stats_country_type", "stats", ["stat_type", "country"], unique=False)
    op.drop_index(op.f("ix_station_code"), table_name="station")
    op.create_index("ix_station_code", "station", ["code"], unique=False)
    op.add_column("milestones", sa.Column("facility_id", sa.TEXT(), autoincrement=False, nullable=True))
    op.drop_constraint(None, "milestones", type_="foreignkey")
    op.alter_column("milestones", "fueltech_id", existing_type=sa.Text(), type_=sa.VARCHAR(), existing_nullable=True)
    op.alter_column("milestones", "network_id", existing_type=sa.Text(), type_=sa.VARCHAR(), existing_nullable=True)
    op.alter_column("milestones", "record_id", existing_type=sa.Text(), type_=sa.UUID(), existing_nullable=False)
    op.drop_column("milestones", "fueltech_group_id")
    op.drop_column("milestones", "network_region")
    op.drop_index("idx_location_boundary", table_name="location", postgresql_using="gist")
    op.drop_constraint("fk_facility_station_code", "facility", type_="foreignkey")
    op.create_foreign_key(
        "fk_facility_station_code", "facility", "station", ["station_id"], ["id"], ondelete="CASCADE"
    )
    op.drop_index(op.f("ix_at_network_flows_v3_trading_interval"), table_name="at_network_flows_v3")
    op.drop_index(op.f("ix_at_network_flows_v3_network_region"), table_name="at_network_flows_v3")
    op.drop_index(op.f("ix_at_network_flows_v3_network_id"), table_name="at_network_flows_v3")
    op.drop_index("idx_at_network_flowsy_v3_network_id_trading_interval", table_name="at_network_flows_v3")
    op.drop_index("idx_at_network_flows_v3_trading_interval_facility_code", table_name="at_network_flows_v3")
    op.drop_table("at_network_flows_v3")
    # ### end Alembic commands ###
