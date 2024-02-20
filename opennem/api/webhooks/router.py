import logging

from fastapi import APIRouter, Request
from fastapi_versionizer.versionizer import api_version
from starlette.exceptions import HTTPException

from opennem import settings
from opennem.controllers.sanity import parse_sanity_webhook

logger = logging.getLogger("opennem.api.webhooks.router")

router = APIRouter(tags=["Webhooks"], include_in_schema=False)


@router.post(
    "/sanity/{webhook_secret}",
    # response_model=APIV4ResponseSchema,
    response_model_exclude_unset=True,
    description="Webhooks",
)
@api_version(4)
async def get_milestones(webhook_secret: str, request: Request) -> str:
    """Get a list of milestones"""

    if webhook_secret != settings.webhook_secret:
        raise HTTPException(status_code=404, detail="Not Found")

    request_json = await request.json()

    logger.debug(request_json)

    if "_type" not in request_json:
        raise HTTPException(status_code=400, detail="Invalid request no _type field present")

    try:
        parse_sanity_webhook(request_json)
    except Exception as e:
        logger.error(f"Error parsing webhook: {e}")
        raise HTTPException(status_code=500, detail="Server Error") from e

    return "OK"
