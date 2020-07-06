"""Schema v0.4.12

Revision ID: 52917cba6ecb
Revises: 
Create Date: 2020-07-07 12:13:14.337018

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "52917cba6ecb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade(engine_name):
    globals()["upgrade_%s" % engine_name]()


def downgrade(engine_name):
    globals()["downgrade_%s" % engine_name]()


def upgrade_opennem():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "fueltech",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("label", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("code"),
    )
    op.create_table(
        "nem_dispatch_case_solution",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("SETTLEMENTDATE", sa.DateTime(), nullable=True),
        sa.Column("RUNO", sa.Integer(), nullable=False),
        sa.Column("INTERVENTION", sa.Integer(), nullable=True),
        sa.Column("CASESUBTYPE", sa.Integer(), nullable=True),
        sa.Column("SOLUTIONSTATUS", sa.Integer(), nullable=True),
        sa.Column("SPDVERSION", sa.Integer(), nullable=True),
        sa.Column("NONPHYSICALLOSSES", sa.Integer(), nullable=True),
        sa.Column("TOTALOBJECTIVE", sa.Numeric(), nullable=True),
        sa.Column("TOTALAREAGENVIOLATION", sa.Integer(), nullable=True),
        sa.Column("TOTALINTERCONNECTORVIOLATION", sa.Integer(), nullable=True),
        sa.Column("TOTALGENERICVIOLATION", sa.Integer(), nullable=True),
        sa.Column("TOTALRAMPRATEVIOLATION", sa.Integer(), nullable=True),
        sa.Column("TOTALUNITMWCAPACITYVIOLATION", sa.Integer(), nullable=True),
        sa.Column("TOTAL5MINVIOLATION", sa.Integer(), nullable=True),
        sa.Column("TOTALREGVIOLATION", sa.Integer(), nullable=True),
        sa.Column("TOTAL6SECVIOLATION", sa.Integer(), nullable=True),
        sa.Column("TOTAL60SECVIOLATION", sa.Integer(), nullable=True),
        sa.Column("TOTALASPROFILEVIOLATION", sa.Integer(), nullable=True),
        sa.Column("TOTALFASTSTARTVIOLATION", sa.Integer(), nullable=True),
        sa.Column("TOTALENERGYOFFERVIOLATION", sa.Integer(), nullable=True),
        sa.Column("LASTCHANGED", sa.Integer(), nullable=True),
        sa.Column("SWITCHRUNINITIALSTATUS", sa.Integer(), nullable=True),
        sa.Column("SWITCHRUNBESTSTATUS", sa.Integer(), nullable=True),
        sa.Column("SWITCHRUNBESTSTATUS_INT", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_nem_dispatch_case_solution_SETTLEMENTDATE"),
        "nem_dispatch_case_solution",
        ["SETTLEMENTDATE"],
        unique=False,
    )
    op.create_index(
        "nem_dispatch_case_solution_uniq",
        "nem_dispatch_case_solution",
        ["SETTLEMENTDATE"],
        unique=True,
    )
    op.create_table(
        "nem_dispatch_constraint",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("SETTLEMENTDATE", sa.Integer(), nullable=False),
        sa.Column("RUNNO", sa.Integer(), nullable=False),
        sa.Column("CONSTRAINTID", sa.Text(), nullable=True),
        sa.Column(
            "DISPATCHINTERVAL", sa.DateTime(timezone=True), nullable=False
        ),
        sa.Column("INTERVENTION", sa.Numeric(), nullable=True),
        sa.Column("RHS", sa.Numeric(), nullable=True),
        sa.Column("MARGINALVALUE", sa.Integer(), nullable=True),
        sa.Column("VIOLATIONDEGREE", sa.Integer(), nullable=True),
        sa.Column("LASTCHANGED", sa.DateTime(timezone=True), nullable=True),
        sa.Column("DUID", sa.Text(), nullable=True),
        sa.Column(
            "GENCONID_EFFECTIVEDATE", sa.DateTime(timezone=True), nullable=True
        ),
        sa.Column("GENCONID_VERSIONNO", sa.Integer(), nullable=False),
        sa.Column("LHS", sa.Numeric(), nullable=True),
        sa.PrimaryKeyConstraint("SETTLEMENTDATE", "DISPATCHINTERVAL"),
    )
    op.create_table(
        "nem_dispatch_interconnection",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("SETTLEMENTDATE", sa.Integer(), nullable=False),
        sa.Column("RUNNO", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("SETTLEMENTDATE"),
    )
    op.create_table(
        "nem_dispatch_interconnector_res",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("SETTLEMENTDATE", sa.Integer(), nullable=False),
        sa.Column("RUNNO", sa.Integer(), nullable=False),
        sa.Column("INTERCONNECTORID", sa.Text(), nullable=False),
        sa.Column(
            "DISPATCHINTERVAL", sa.DateTime(timezone=True), nullable=False
        ),
        sa.Column("INTERVENTION", sa.Numeric(), nullable=True),
        sa.Column("METEREDMWFLOW", sa.Numeric(), nullable=True),
        sa.Column("MWFLOW", sa.Numeric(), nullable=True),
        sa.Column("MWLOSSES", sa.Numeric(), nullable=True),
        sa.Column("MARGINALVALUE", sa.Numeric(), nullable=True),
        sa.Column("VIOLATIONDEGREE", sa.Numeric(), nullable=True),
        sa.Column("LASTCHANGED", sa.DateTime(timezone=True), nullable=False),
        sa.Column("EXPORTLIMIT", sa.Numeric(), nullable=True),
        sa.Column("IMPORTLIMIT", sa.Numeric(), nullable=True),
        sa.Column("MARGINALLOSS", sa.Numeric(), nullable=True),
        sa.Column("EXPORTGENCONID", sa.Text(), nullable=False),
        sa.Column("IMPORTGENCONID", sa.Text(), nullable=False),
        sa.Column("FCASEXPORTLIMIT", sa.Numeric(), nullable=True),
        sa.Column("FCASIMPORTLIMIT", sa.Numeric(), nullable=True),
        sa.Column(
            "LOCAL_PRICE_ADJUSTMENT_EXPORT", sa.Numeric(), nullable=True
        ),
        sa.Column("LOCALLY_CONSTRAINED_EXPORT", sa.Numeric(), nullable=True),
        sa.Column(
            "LOCAL_PRICE_ADJUSTMENT_IMPORT", sa.Numeric(), nullable=True
        ),
        sa.Column("LOCALLY_CONSTRAINED_IMPORT", sa.Numeric(), nullable=True),
        sa.PrimaryKeyConstraint(
            "SETTLEMENTDATE", "INTERCONNECTORID", "DISPATCHINTERVAL"
        ),
    )
    op.create_table(
        "nem_dispatch_price",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("SETTLEMENTDATE", sa.DateTime(), nullable=True),
        sa.Column("DUID", sa.Text(), nullable=True),
        sa.Column(
            "SCADAVALUE", sa.NUMERIC(precision=10, scale=6), nullable=True
        ),
        sa.Column("REGIONID", sa.Text(), nullable=True),
        sa.Column("RUNO", sa.Integer(), nullable=False),
        sa.Column("DISPATCHINTERVAL", sa.Integer(), nullable=False),
        sa.Column("INTERVENTION", sa.Integer(), nullable=False),
        sa.Column("RRP", sa.Integer(), nullable=False),
        sa.Column("EEP", sa.Integer(), nullable=False),
        sa.Column("ROP", sa.Integer(), nullable=False),
        sa.Column("APCFLAG", sa.Integer(), nullable=False),
        sa.Column("MARKETSUSPENDEDFLAG", sa.Integer(), nullable=False),
        sa.Column("LASTCHANGED", sa.DateTime(timezone=True), nullable=False),
        sa.Column("RAISE6SECRRP", sa.Integer(), nullable=False),
        sa.Column("RAISE6SECROP", sa.Integer(), nullable=False),
        sa.Column("RAISE6SECAPCFLAG", sa.Integer(), nullable=False),
        sa.Column("RAISE60SECRRP", sa.Integer(), nullable=False),
        sa.Column("RAISE60SECROP", sa.Integer(), nullable=False),
        sa.Column("RAISE60SECAPCFLAG", sa.Integer(), nullable=False),
        sa.Column("RAISE5MINRRP", sa.Integer(), nullable=False),
        sa.Column("RAISE5MINROP", sa.Integer(), nullable=False),
        sa.Column("RAISE5MINAPCFLAG", sa.Integer(), nullable=False),
        sa.Column("RAISEREGRRP", sa.Integer(), nullable=False),
        sa.Column("RAISEREGROP", sa.Integer(), nullable=False),
        sa.Column("RAISEREGAPCFLAG", sa.Integer(), nullable=False),
        sa.Column("LOWER6SECRRP", sa.Integer(), nullable=False),
        sa.Column("LOWER6SECROP", sa.Integer(), nullable=False),
        sa.Column("LOWER6SECAPCFLAG", sa.Integer(), nullable=False),
        sa.Column("LOWER60SECRRP", sa.Integer(), nullable=False),
        sa.Column("LOWER60SECROP", sa.Integer(), nullable=False),
        sa.Column("LOWER60SECAPCFLAG", sa.Integer(), nullable=False),
        sa.Column("LOWER5MINRRP", sa.Integer(), nullable=False),
        sa.Column("LOWER5MINROP", sa.Integer(), nullable=False),
        sa.Column("LOWER5MINAPCFLAG", sa.Integer(), nullable=False),
        sa.Column("LOWERREGRRP", sa.Integer(), nullable=False),
        sa.Column("LOWERREGROP", sa.Integer(), nullable=False),
        sa.Column("LOWERREGAPCFLAG", sa.Integer(), nullable=False),
        sa.Column("PRICE_STATUS", sa.Integer(), nullable=False),
        sa.Column("PRE_AP_ENERGY_PRICE", sa.Integer(), nullable=False),
        sa.Column("PRE_AP_RAISE6_PRICE", sa.Integer(), nullable=False),
        sa.Column("PRE_AP_RAISE60_PRICE", sa.Integer(), nullable=False),
        sa.Column("PRE_AP_RAISE5MIN_PRICE", sa.Integer(), nullable=False),
        sa.Column("PRE_AP_RAISEREG_PRICE", sa.Integer(), nullable=False),
        sa.Column("PRE_AP_LOWER6_PRICE", sa.Integer(), nullable=False),
        sa.Column("PRE_AP_LOWER60_PRICE", sa.Integer(), nullable=False),
        sa.Column("PRE_AP_LOWER5MIN_PRICE", sa.Integer(), nullable=False),
        sa.Column("PRE_AP_LOWERREG_PRICE", sa.Integer(), nullable=False),
        sa.Column("CUMUL_PRE_AP_ENERGY_PRICE", sa.Integer(), nullable=False),
        sa.Column("CUMUL_PRE_AP_RAISE6_PRICE", sa.Integer(), nullable=False),
        sa.Column("CUMUL_PRE_AP_RAISE60_PRICE", sa.Integer(), nullable=False),
        sa.Column(
            "CUMUL_PRE_AP_RAISE5MIN_PRICE", sa.Integer(), nullable=False
        ),
        sa.Column("CUMUL_PRE_AP_RAISEREG_PRICE", sa.Integer(), nullable=False),
        sa.Column("CUMUL_PRE_AP_LOWER6_PRICE", sa.Integer(), nullable=False),
        sa.Column("CUMUL_PRE_AP_LOWER60_PRICE", sa.Integer(), nullable=False),
        sa.Column(
            "CUMUL_PRE_AP_LOWER5MIN_PRICE", sa.Integer(), nullable=False
        ),
        sa.Column("CUMUL_PRE_AP_LOWERREG_PRICE", sa.Integer(), nullable=False),
        sa.Column("OCD_STATUS", sa.Text(), nullable=False),
        sa.Column("MII_STATUS", sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_nem_dispatch_price_DUID"),
        "nem_dispatch_price",
        ["DUID"],
        unique=False,
    )
    op.create_index(
        op.f("ix_nem_dispatch_price_REGIONID"),
        "nem_dispatch_price",
        ["REGIONID"],
        unique=False,
    )
    op.create_index(
        op.f("ix_nem_dispatch_price_SETTLEMENTDATE"),
        "nem_dispatch_price",
        ["SETTLEMENTDATE"],
        unique=False,
    )
    op.create_index(
        "nem_dispatch_price_uniq",
        "nem_dispatch_price",
        ["SETTLEMENTDATE", "DUID"],
        unique=True,
    )
    op.create_table(
        "nem_dispatch_region_sum",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("SETTLEMENTDATE", sa.Integer(), nullable=False),
        sa.Column("RUNNO", sa.Integer(), nullable=False),
        sa.Column("REGIONID", sa.Text(), nullable=False),
        sa.Column(
            "DISPATCHINTERVAL", sa.DateTime(timezone=True), nullable=False
        ),
        sa.Column("INTERVENTION", sa.Integer(), nullable=False),
        sa.Column("TOTALDEMAND", sa.Numeric(), nullable=False),
        sa.Column("AVAILABLEGENERATION", sa.Numeric(), nullable=True),
        sa.Column("AVAILABLELOAD", sa.Numeric(), nullable=True),
        sa.Column("DEMANDFORECAST", sa.Numeric(), nullable=True),
        sa.Column("DISPATCHABLEGENERATION", sa.Numeric(), nullable=True),
        sa.Column("DISPATCHABLELOAD", sa.Numeric(), nullable=True),
        sa.Column("NETINTERCHANGE", sa.Numeric(), nullable=True),
        sa.Column("EXCESSGENERATION", sa.Numeric(), nullable=True),
        sa.Column("LOWER5MINDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("LOWER5MINIMPORT", sa.Numeric(), nullable=True),
        sa.Column("LOWER5MINLOCALDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("LOWER5MINLOCALPRICE", sa.Numeric(), nullable=True),
        sa.Column("LOWER5MINLOCALREQ", sa.Numeric(), nullable=True),
        sa.Column("LOWER5MINPRICE", sa.Numeric(), nullable=True),
        sa.Column("LOWER5MINREQ", sa.Numeric(), nullable=True),
        sa.Column("LOWER5MINSUPPLYPRICE", sa.Numeric(), nullable=True),
        sa.Column("LOWER60SECDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("LOWER60SECIMPORT", sa.Numeric(), nullable=True),
        sa.Column("LOWER60SECLOCALDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("LOWER60SECLOCALPRICE", sa.Numeric(), nullable=True),
        sa.Column("LOWER60SECLOCALREQ", sa.Numeric(), nullable=True),
        sa.Column("LOWER60SECPRICE", sa.Numeric(), nullable=True),
        sa.Column("LOWER60SECREQ", sa.Numeric(), nullable=True),
        sa.Column("LOWER60SECSUPPLYPRICE", sa.Numeric(), nullable=True),
        sa.Column("LOWER6SECDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("LOWER6SECIMPORT", sa.Numeric(), nullable=True),
        sa.Column("LOWER6SECLOCALDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("LOWER6SECLOCALPRICE", sa.Numeric(), nullable=True),
        sa.Column("LOWER6SECLOCALREQ", sa.Numeric(), nullable=True),
        sa.Column("LOWER6SECPRICE", sa.Numeric(), nullable=True),
        sa.Column("LOWER6SECREQ", sa.Numeric(), nullable=True),
        sa.Column("LOWER6SECSUPPLYPRICE", sa.Numeric(), nullable=True),
        sa.Column("RAISE5MINDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("RAISE5MINIMPORT", sa.Numeric(), nullable=True),
        sa.Column("RAISE5MINLOCALDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("RAISE5MINLOCALPRICE", sa.Numeric(), nullable=True),
        sa.Column("RAISE5MINLOCALREQ", sa.Numeric(), nullable=True),
        sa.Column("RAISE5MINPRICE", sa.Numeric(), nullable=True),
        sa.Column("RAISE5MINREQ", sa.Numeric(), nullable=True),
        sa.Column("RAISE5MINSUPPLYPRICE", sa.Numeric(), nullable=True),
        sa.Column("RAISE60SECDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("RAISE60SECIMPORT", sa.Numeric(), nullable=True),
        sa.Column("RAISE60SECLOCALDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("RAISE60SECLOCALPRICE", sa.Numeric(), nullable=True),
        sa.Column("RAISE60SECLOCALREQ", sa.Numeric(), nullable=True),
        sa.Column("RAISE60SECPRICE", sa.Numeric(), nullable=True),
        sa.Column("RAISE60SECREQ", sa.Numeric(), nullable=True),
        sa.Column("RAISE60SECSUPPLYPRICE", sa.Numeric(), nullable=True),
        sa.Column("RAISE6SECDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("RAISE6SECIMPORT", sa.Numeric(), nullable=True),
        sa.Column("RAISE6SECLOCALDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("RAISE6SECLOCALPRICE", sa.Numeric(), nullable=True),
        sa.Column("RAISE6SECLOCALREQ", sa.Numeric(), nullable=True),
        sa.Column("RAISE6SECPRICE", sa.Numeric(), nullable=True),
        sa.Column("RAISE6SECREQ", sa.Numeric(), nullable=True),
        sa.Column("RAISE6SECSUPPLYPRICE", sa.Numeric(), nullable=True),
        sa.Column("AGGEGATEDISPATCHERROR", sa.Numeric(), nullable=True),
        sa.Column("AGGREGATEDISPATCHERROR", sa.Numeric(), nullable=True),
        sa.Column("LASTCHANGED", sa.Numeric(), nullable=True),
        sa.Column("INITIALSUPPLY", sa.Numeric(), nullable=True),
        sa.Column("CLEAREDSUPPLY", sa.Numeric(), nullable=True),
        sa.Column("LOWERREGIMPORT", sa.Numeric(), nullable=True),
        sa.Column("LOWERREGLOCALDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("LOWERREGLOCALREQ", sa.Numeric(), nullable=True),
        sa.Column("LOWERREGREQ", sa.Numeric(), nullable=True),
        sa.Column("RAISEREGIMPORT", sa.Numeric(), nullable=True),
        sa.Column("RAISEREGLOCALDISPATCH", sa.Numeric(), nullable=True),
        sa.Column("RAISEREGLOCALREQ", sa.Numeric(), nullable=True),
        sa.Column("RAISEREGREQ", sa.Numeric(), nullable=True),
        sa.Column("RAISE5MINLOCALVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("RAISEREGLOCALVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("RAISE60SECLOCALVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("RAISE6SECLOCALVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("LOWER5MINLOCALVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("LOWERREGLOCALVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("LOWER60SECLOCALVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("LOWER6SECLOCALVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("RAISE5MINVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("RAISEREGVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("RAISE60SECVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("RAISE6SECVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("LOWER5MINVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("LOWERREGVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("LOWER60SECVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("LOWER6SECVIOLATION", sa.Numeric(), nullable=True),
        sa.Column("RAISE6SECACTUALAVAILABILITY", sa.Numeric(), nullable=True),
        sa.Column("RAISE60SECACTUALAVAILABILITY", sa.Numeric(), nullable=True),
        sa.Column("RAISE5MINACTUALAVAILABILITY", sa.Numeric(), nullable=True),
        sa.Column("RAISEREGACTUALAVAILABILITY", sa.Numeric(), nullable=True),
        sa.Column("LOWER6SECACTUALAVAILABILITY", sa.Numeric(), nullable=True),
        sa.Column("LOWER60SECACTUALAVAILABILITY", sa.Numeric(), nullable=True),
        sa.Column("LOWER5MINACTUALAVAILABILITY", sa.Numeric(), nullable=True),
        sa.Column("LOWERREGACTUALAVAILABILITY", sa.Numeric(), nullable=True),
        sa.Column("LORSURPLUS", sa.Numeric(), nullable=True),
        sa.Column("LRCSURPLUS", sa.Numeric(), nullable=True),
        sa.Column("TOTALINTERMITTENTGENERATION", sa.Numeric(), nullable=True),
        sa.Column("DEMAND_AND_NONSCHEDGEN", sa.Numeric(), nullable=True),
        sa.Column("UIGF", sa.Numeric(), nullable=True),
        sa.Column("SEMISCHEDULE_CLEAREDMW", sa.Numeric(), nullable=True),
        sa.Column("SEMISCHEDULE_COMPLIANCEMW", sa.Numeric(), nullable=True),
        sa.PrimaryKeyConstraint(
            "SETTLEMENTDATE", "REGIONID", "DISPATCHINTERVAL"
        ),
    )
    op.create_table(
        "nem_dispatch_unit_scada",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("SETTLEMENTDATE", sa.DateTime(), nullable=True),
        sa.Column("DUID", sa.Text(), nullable=True),
        sa.Column(
            "SCADAVALUE", sa.NUMERIC(precision=10, scale=6), nullable=True
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_nem_dispatch_unit_scada_DUID"),
        "nem_dispatch_unit_scada",
        ["DUID"],
        unique=False,
    )
    op.create_index(
        op.f("ix_nem_dispatch_unit_scada_SETTLEMENTDATE"),
        "nem_dispatch_unit_scada",
        ["SETTLEMENTDATE"],
        unique=False,
    )
    op.create_index(
        "nem_dispatch_unit_scada_uniq",
        "nem_dispatch_unit_scada",
        ["SETTLEMENTDATE", "DUID"],
        unique=True,
    )
    op.create_table(
        "wem_balancing_summary",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("trading_interval", sa.DateTime(), nullable=False),
        sa.Column("forecast_load", sa.Numeric(), nullable=True),
        sa.Column("generation_scheduled", sa.Numeric(), nullable=True),
        sa.Column("generation_non_scheduled", sa.Numeric(), nullable=True),
        sa.Column("generation_total", sa.Numeric(), nullable=True),
        sa.Column("price", sa.Numeric(), nullable=True),
        sa.PrimaryKeyConstraint("trading_interval"),
    )
    op.create_index(
        op.f("ix_wem_balancing_summary_trading_interval"),
        "wem_balancing_summary",
        ["trading_interval"],
        unique=False,
    )
    op.create_table(
        "wem_participant",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("name", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("code"),
    )
    op.create_index(
        op.f("ix_wem_participant_code"),
        "wem_participant",
        ["code"],
        unique=False,
    )
    op.create_index(
        op.f("ix_wem_participant_name"),
        "wem_participant",
        ["name"],
        unique=False,
    )
    op.create_table(
        "wem_facility",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("code", sa.Text(), nullable=False),
        sa.Column("participant_id", sa.Text(), nullable=True),
        sa.Column("fueltech_id", sa.Text(), nullable=True),
        sa.Column("active", sa.Boolean(), nullable=True),
        sa.Column("capacity_credits", sa.Numeric(), nullable=True),
        sa.Column("capacity_maximum", sa.Numeric(), nullable=True),
        sa.Column("registered", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["fueltech_id"],
            ["fueltech.code"],
            name="fk_wem_facility_fueltech_id",
        ),
        sa.ForeignKeyConstraint(
            ["participant_id"],
            ["wem_participant.code"],
            name="fk_facility_participant_id",
        ),
        sa.PrimaryKeyConstraint("code"),
    )
    op.create_table(
        "wem_facility_scada",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("trading_interval", sa.DateTime(), nullable=False),
        sa.Column("facility_id", sa.Text(), nullable=False),
        sa.Column("generated", sa.Numeric(), nullable=True),
        sa.Column("eoi_quantity", sa.Numeric(), nullable=True),
        sa.ForeignKeyConstraint(
            ["facility_id"],
            ["wem_facility.code"],
            name="fk_facility_scada_facility_id",
        ),
        sa.PrimaryKeyConstraint("trading_interval", "facility_id"),
    )
    op.create_index(
        op.f("ix_wem_facility_scada_trading_interval"),
        "wem_facility_scada",
        ["trading_interval"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade_opennem():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_wem_facility_scada_trading_interval"),
        table_name="wem_facility_scada",
    )
    op.drop_table("wem_facility_scada")
    op.drop_table("wem_facility")
    op.drop_index(
        op.f("ix_wem_participant_name"), table_name="wem_participant"
    )
    op.drop_index(
        op.f("ix_wem_participant_code"), table_name="wem_participant"
    )
    op.drop_table("wem_participant")
    op.drop_index(
        op.f("ix_wem_balancing_summary_trading_interval"),
        table_name="wem_balancing_summary",
    )
    op.drop_table("wem_balancing_summary")
    op.drop_index(
        "nem_dispatch_unit_scada_uniq", table_name="nem_dispatch_unit_scada"
    )
    op.drop_index(
        op.f("ix_nem_dispatch_unit_scada_SETTLEMENTDATE"),
        table_name="nem_dispatch_unit_scada",
    )
    op.drop_index(
        op.f("ix_nem_dispatch_unit_scada_DUID"),
        table_name="nem_dispatch_unit_scada",
    )
    op.drop_table("nem_dispatch_unit_scada")
    op.drop_table("nem_dispatch_region_sum")
    op.drop_index("nem_dispatch_price_uniq", table_name="nem_dispatch_price")
    op.drop_index(
        op.f("ix_nem_dispatch_price_SETTLEMENTDATE"),
        table_name="nem_dispatch_price",
    )
    op.drop_index(
        op.f("ix_nem_dispatch_price_REGIONID"), table_name="nem_dispatch_price"
    )
    op.drop_index(
        op.f("ix_nem_dispatch_price_DUID"), table_name="nem_dispatch_price"
    )
    op.drop_table("nem_dispatch_price")
    op.drop_table("nem_dispatch_interconnector_res")
    op.drop_table("nem_dispatch_interconnection")
    op.drop_table("nem_dispatch_constraint")
    op.drop_index(
        "nem_dispatch_case_solution_uniq",
        table_name="nem_dispatch_case_solution",
    )
    op.drop_index(
        op.f("ix_nem_dispatch_case_solution_SETTLEMENTDATE"),
        table_name="nem_dispatch_case_solution",
    )
    op.drop_table("nem_dispatch_case_solution")
    op.drop_table("fueltech")
    # ### end Alembic commands ###
