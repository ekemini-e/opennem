"""
RecordReactor utils
"""

import operator

from opennem.core.fueltech_group import get_fueltech_group
from opennem.core.network_regions import get_network_region_name
from opennem.core.units import get_unit_by_value
from opennem.recordreactor.schema import (
    MilestoneAggregate,
    MilestoneMetric,
    MilestonePeriod,
    MilestoneRecordOutputSchema,
    MilestoneRecordSchema,
)
from opennem.schema.units import UnitDefinition
from opennem.utils.seasons import map_date_start_to_season


def translate_bucket_size_to_english(bucket_size: str) -> str:
    if bucket_size == "year":
        return "annual"
    elif bucket_size == "quarter":
        return "quarterly"
    elif bucket_size == "month":
        return "monthly"
    elif bucket_size == "week":
        return "weekly"
    elif bucket_size == "day":
        return "daily"
    elif bucket_size == "financial_year":
        return "financial year"
    else:
        return bucket_size


def check_milestone_is_new(milestone: MilestoneRecordSchema, milestone_previous: MilestoneRecordOutputSchema) -> bool:
    """
    Checks if the given milestone is new or has changed

    Args:
        milestone (MilestoneRecord): The milestone record
        milestone_state (dict[str, MilestoneRecord]): The milestone state

    Returns:
        bool: True if the milestone is new, False if it has changed
    """
    _op = operator.gt if milestone.aggregate in [MilestoneAggregate.high] else operator.lt

    if not milestone.value:
        return False

    return _op(milestone.value, milestone_previous.value)


def get_record_description(
    milestone: MilestoneRecordSchema,
    include_value: bool = False,
) -> str:
    """get a record description"""

    record_description_components = [
        map_date_start_to_season(milestone.interval).capitalize()
        if milestone.period is MilestonePeriod.season
        else translate_bucket_size_to_english(milestone.period).capitalize()
        if milestone.period
        else None,
        f"{milestone.fueltech.label.lower()}" if milestone.fueltech else None,
        f"{milestone.metric.value.lower()}" if milestone.metric else None,
        f"{milestone.aggregate.value.lower()}" if milestone.aggregate else None,
        "record for",
        milestone.network.code,
        # network region
        f"in {get_network_region_name(milestone.network_region)}"
        if milestone.network_region
        else f"in {milestone.network_region}"
        if milestone.network_region
        else None,
        # value
        f"({round(milestone.value, 2) if milestone.value else ''} {milestone.unit.value if milestone.unit else ''})"
        if include_value
        else None,
    ]

    # remove empty items from record id components list and join with a period
    record_description = " ".join(filter(None, record_description_components))

    return record_description


def get_record_unit_by_metric(metric: MilestoneMetric) -> UnitDefinition:
    """get a record unit by metric"""
    if metric == MilestoneMetric.demand:
        return get_unit_by_value("MW")
    elif metric == MilestoneMetric.price:
        return get_unit_by_value("AUD")
    elif metric == MilestoneMetric.power:
        return get_unit_by_value("MW")
    elif metric == MilestoneMetric.energy:
        return get_unit_by_value("MWh")
    elif metric == MilestoneMetric.emissions:
        return get_unit_by_value("tCO2e")
    else:
        raise ValueError(f"Invalid metric: {metric}")


if __name__ == "__main__":
    from datetime import datetime

    from opennem.schema.network import NetworkNEM

    test_record = MilestoneRecordSchema(
        interval=datetime.now(),
        aggregate=MilestoneAggregate.high,
        metric=MilestoneMetric.demand,
        period=MilestonePeriod.year,
        value=100,
        unit=get_unit_by_value("MW"),
        network=NetworkNEM,
        network_region="NSW1",
        fueltech=None,
    )

    print(get_record_description(test_record))

    test_record2 = MilestoneRecordSchema(
        interval=datetime.now(),
        aggregate=MilestoneAggregate.low,
        metric=MilestoneMetric.energy,
        period=MilestonePeriod.financial_year,
        value=100,
        unit=get_unit_by_value("MWh"),
        network=NetworkNEM,
        network_region="NSW1",
        fueltech=get_fueltech_group("coal"),
    )

    print(get_record_description(test_record2))
