"""
Exports all approved facilites to a static JSON file for use on the OpenNEM
and OpenElectricity websites on the facilities page.

"""

import asyncio

from opennem.api.schema import APIV4ResponseSchema
from opennem.cms.importer import get_cms_facilities
from opennem.exporter.storage_bucket import cloudflare_uploader
from opennem.utils.dates import get_today_opennem
from opennem.utils.version import get_version


async def export_facilities_static() -> None:
    """Export facilities to a static JSON file"""

    # get all facilities
    facilities = get_cms_facilities()

    # remove 'battery' units
    facilities_clean = []

    for facility in facilities:
        units = [u for u in facility.units if u.fueltech_id != "battery"]
        facility.units = units
        facilities_clean.append(facility)

    model_output = APIV4ResponseSchema(
        version=get_version(),
        created_at=get_today_opennem(),
        success=True,
        total_records=len(facilities_clean),
        data=facilities_clean,
    )

    await cloudflare_uploader.upload_content(
        model_output.model_dump_json(exclude_unset=True, exclude_none=True),
        "/v4/facilities/au_facilities.json",
        content_type="application/json",
    )


if __name__ == "__main__":
    asyncio.run(export_facilities_static())
