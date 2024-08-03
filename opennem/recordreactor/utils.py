"""
RecordReactor utils
"""

import operator

from opennem.core.units import get_unit_by_value
from opennem.recordreactor.schema import MilestoneAggregate, MilestoneMetric, MilestoneRecord, MilestoneSchema
from opennem.schema.units import UnitDefinition


def check_milestone_is_new(milestone: MilestoneSchema, milestone_previous: MilestoneRecord, data: dict[str, str | float]) -> bool:
    """
    Checks if the given milestone is new or has changed

    Args:
        milestone (MilestoneRecord): The milestone record
        milestone_state (dict[str, MilestoneRecord]): The milestone state

    Returns:
        bool: True if the milestone is new, False if it has changed
    """
    _op = operator.gt if milestone.aggregate in [MilestoneAggregate.high] else operator.lt

    data_key = f"{milestone.metric.value}_{milestone.aggregate.value}"
    data_value = data[data_key]

    if not data_value:
        return False

    return _op(data_value, milestone_previous.value)


def get_record_description(
    milestone: MilestoneRecord,
) -> str:
    """get a record description"""
    record_description_components = [
        f"{milestone.metric.value.capitalize()}" if milestone.metric else None,
        f"{milestone.value_unit.value}" if milestone.value_unit else None,
        f"{milestone.aggregate.value.capitalize()}" if milestone.aggregate else None,
        f"{milestone.unit_code}" if milestone.unit_code else None,
        f"for {milestone.fueltech_id}" if milestone.fueltech_id else None,
        milestone.period.lower() if milestone.period else None,
        "record for",
        milestone.network_id,
        f"in {milestone.network_region}" if milestone.network_region else None,
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
