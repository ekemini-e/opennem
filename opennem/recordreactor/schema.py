"""OpenNEM Schema class for a milestone

see matching ORM schema in database. This applies within record reactor and the API output
"""

from datetime import datetime
from enum import Enum

from pydantic import UUID4, BaseModel, Field, computed_field

from opennem.schema.fueltech import FueltechSchema
from opennem.schema.fueltech_group import FueltechGroupSchema
from opennem.schema.network import NetworkNEM, NetworkSchema, NetworkWEM
from opennem.schema.units import UnitDefinition

MILESTONE_SUPPORTED_NETWORKS = [NetworkNEM, NetworkWEM]


class MilestoneAggregate(str, Enum):
    low = "low"
    high = "high"


class MilestoneMetric(str, Enum):
    demand = "demand"
    price = "price"
    power = "power"
    energy = "energy"
    emissions = "emissions"


class MilestonePeriod(str, Enum):
    interval = "interval"
    day = "day"
    week = "week"
    month = "month"
    quarter = "quarter"
    year = "year"
    financial_year = "financial_year"


class MilestoneFueltech(str, Enum):
    coal = "coal"
    gas = "gas"
    wind = "wind"
    solar = "solar"
    battery_charging = "battery_charging"
    battery_discharging = "battery_discharging"
    hydro = "hydro"
    distillate = "distillate"
    biomass = "biomass"
    pumped = "pumps"


class MilestoneSchema(BaseModel):
    interval: datetime
    aggregate: MilestoneAggregate
    metric: MilestoneMetric
    period: MilestonePeriod
    unit: UnitDefinition
    network: NetworkSchema
    network_region: str | None = None
    fueltech: FueltechGroupSchema | None = None
    value: int | float | None = None

    @computed_field
    @property
    def record_id(self) -> str:
        """calculate the record_id from the milestone record"""
        return get_milestone_record_id(self)


class MilestoneRecordSchema(BaseModel):
    record_id: str
    interval: datetime
    instance_id: UUID4
    aggregate: MilestoneAggregate
    metric: MilestoneMetric | None = None
    period: str | None = None
    significance: int
    value: int | float
    unit: UnitDefinition | None = Field(exclude=True)
    network: NetworkSchema = Field(exclude=True)
    network_region: str | None = None
    fueltech_id: FueltechSchema | str | None = None
    description: str | None = None
    description_long: str | None = None
    previous_instance_id: UUID4 | None = None
    history: list["MilestoneRecordSchema"] | None = None

    @computed_field
    @property
    def value_unit(self) -> str | None:
        return self.unit.value if self.unit else None

    @computed_field
    @property
    def network_id(self) -> str:
        return (
            self.network.code
            if self.network and isinstance(self.network, NetworkSchema)
            else self.network
            if self.network
            else ""
        )

    @property
    def unit_code(self) -> str | None:
        return self.unit.name if self.unit else None


def get_milestone_network_id_map(network_id: str) -> str:
    """Get a network id map"""
    network_id_map = {
        "AEMO_ROOFTOP": "NEM",
        "APVI": "WEM",
    }

    if network_id not in network_id_map:
        return network_id

    return network_id_map[network_id]


def get_milestone_record_id(
    milestone: MilestoneSchema,
) -> str:
    """Get a record id"""
    record_id_components = [
        "au",
        milestone.network.parent_network or milestone.network.code,
        milestone.network_region,
        milestone.fueltech.code if milestone.fueltech else None,
        milestone.metric.value,
        milestone.period.value,
        milestone.aggregate.value,
    ]

    # remove empty items from record id components list and join with a period
    record_id = ".".join(filter(None, record_id_components)).lower()

    return record_id


def get_milestone_period_from_bucket_size(bucket_size: str) -> MilestonePeriod:
    """Get the milestone period from the bucket size"""
    if bucket_size == "interval":
        return MilestonePeriod.interval
    elif bucket_size == "day":
        return MilestonePeriod.day
    elif bucket_size == "week":
        return MilestonePeriod.week
    elif bucket_size == "month":
        return MilestonePeriod.month
    elif bucket_size == "year":
        return MilestonePeriod.year
    else:
        raise ValueError(f"Invalid bucket_size: {bucket_size}")
