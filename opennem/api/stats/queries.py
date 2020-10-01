from datetime import datetime
from typing import List, Tuple

from opennem.core.normalizers import normalize_duid


def duid_in_case(facility_codes: List[str]) -> str:
    return ",".join(
        ["'{}'".format(i) for i in map(normalize_duid, facility_codes)]
    )


INTERVAL_MAP = {
    "1d": {"trunc": "day", "interval": "1 day"},
    "1h": {"trunc": "hour", "interval": "1 hour"},
}

PERIOD_MAP = {"7d": "7 day", "1M": "1 month"}


def get_interval_map(interval: str) -> Tuple[str, str]:
    if interval not in INTERVAL_MAP.keys():
        raise Exception("Invalid interval {} not mapped".format(interval))

    return tuple(INTERVAL_MAP[interval].values())


def get_period_map(period: str) -> str:
    if period not in PERIOD_MAP.keys():
        raise Exception("Invalid period {} not supported".format(period))

    return PERIOD_MAP[period]


def energy_facility(
    facility_codes: List[str],
    network_code: str,
    interval: str = "1d",
    period: str = "7d",
) -> str:

    network_code = network_code.upper()
    trunc, interval_str = get_interval_map(interval)
    period = get_period_map(period)

    __query = """
        with intervals as (
            select generate_series(
                date_trunc('{trunc}', now() AT TIME ZONE 'UTC') - '{period}'::interval,
                date_trunc('{trunc}', now() AT TIME ZONE 'UTC'),
                '{interval}'::interval
            )::timestamp as interval
        )

        select
            i.interval AS trading_day,
            fs.facility_code as facility_code,
            coalesce(sum(fs.eoi_quantity), NULL) as energy_output
        from intervals i
        left join facility_scada fs on date_trunc('{trunc}', fs.trading_interval AT TIME ZONE 'UTC')::timestamp = i.interval
        where
            fs.facility_code in ({facility_codes_parsed})
            and fs.trading_interval > now() AT TIME ZONE 'UTC' - '{period}'::interval
            and fs.network_id = '{network_code}'
        group by 1, 2
        order by 2 asc, 1 asc
    """

    query = __query.format(
        facility_codes_parsed=duid_in_case(facility_codes),
        network_code=network_code,
        trunc=trunc,
        interval=interval_str,
        period=period,
    )

    return query


def energy_year_network(network_code: str = "WEM", year: int = None) -> str:
    if not year:
        year = datetime.today().year

    network_code = network_code.upper()

    return """
        select
            date_trunc('day', fs.trading_interval) AS trading_day,
            max(fs.eoi_quantity) as energy_output,
            f.fueltech_id as fueltech
        from facility_scada fs
        left join facility f on fs.facility_code = f.code
        where
            f.fueltech_id is not null
            and extract('year' from fs.trading_interval) = {year}
            and fs.network_id = '{network_code}'
        group by 1, f.fueltech_id
        order by 1 asc, 2 asc
    """.format(
        year=year, network_code=network_code
    )
