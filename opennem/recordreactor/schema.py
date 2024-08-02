"""OpenNEM Schema class for a milestone

see matching ORM schema in database. This applies within record reactor and the API output
"""

from datetime import datetime
from enum import Enum

from pydantic import UUID4, BaseModel

from opennem.schema.fueltech import FueltechSchema
from opennem.schema.network import NetworkNEM, NetworkSchema, NetworkWEM
from opennem.schema.units import UnitDefinition

MILESTONE_SUPPORTED_NETWORKS = [NetworkNEM, NetworkWEM]


class MilestoneAggregate(str, Enum):
    low = "low"
    average = "average"
    high = "high"


class MilestoneMetric(str, Enum):
    demand = "demand"
    price = "price"
    generation = "generation"
    energy = "energy"
    emissions = "emissions"


class MilestonePeriods(str, Enum):
    interval = "interval"
    day = "day"
    week = "week"
    month = "month"
    quarter = "quarter"
    year = "year"
    financial_year = "financial_year"


class MilestoneRecord(BaseModel):
    record_id: str
    interval: datetime
    instance_id: UUID4
    aggregate: MilestoneAggregate
    metric: MilestoneMetric | None = None
    period: str | None = None
    significance: int
    value: int | float
    value_unit: UnitDefinition | None = None
    network_id: NetworkSchema | str | None = None
    network_region: str | None = None
    fueltech_id: FueltechSchema | None = None
    fueltech_group_id: FueltechSchema | str | None = None
    description: str | None = None
    description_long: str | None = None
    previous_record_id: str | None = None

    @property
    def network_code(self) -> str:
        return self.network_id.code if self.network_id else ""

    @property
    def country(self) -> str:
        return self.country

    @property
    def fueltech_code(self) -> str:
        return self.fueltech_id.code if self.fueltech_id else ""

    @property
    def unit_code(self) -> str | None:
        return self.value_unit.name if self.value_unit else None
