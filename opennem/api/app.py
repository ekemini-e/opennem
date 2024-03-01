"""
OpenNEM API

Primary Router. All the main setup of the API is here.
"""

import logging

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.param_functions import Query
from fastapi.responses import FileResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.backends.redis import RedisBackend
from fastapi_versionizer.versionizer import Versionizer
from redis import asyncio as aioredis
from sqlalchemy.orm import Session
from starlette.requests import Request

from opennem import settings
from opennem.api.dash.router import router as dash_router
from opennem.api.exceptions import OpennemBaseHttpException, OpennemExceptionResponse
from opennem.api.facility.router import router as facility_router
from opennem.api.feedback.router import router as feedback_router
from opennem.api.milestones.router import milestones_router
from opennem.api.schema import APINetworkRegion, APINetworkSchema
from opennem.api.security import api_key_auth
from opennem.api.station.router import router as station_router
from opennem.api.stats.router import router as stats_router
from opennem.api.weather.router import router as weather_router
from opennem.api.webhooks.router import router as webhooks_router
from opennem.core.time import INTERVALS, PERIODS
from opennem.core.units import UNITS
from opennem.db import get_database_session
from opennem.db.models.opennem import FuelTech, Network, NetworkRegion
from opennem.schema.opennem import FueltechSchema, OpennemErrorSchema
from opennem.schema.time import TimeInterval, TimePeriod
from opennem.schema.units import UnitDefinition
from opennem.utils.version import get_version

logger = logging.getLogger("opennem.api")


app = FastAPI(title="OpenNEM", debug=settings.debug, version=get_version(), redoc_url="/docs", docs_url=None)
versions = Versionizer(
    app=app,
    prefix_format="/v{major}",
    semantic_version_format="{major}",
    latest_prefix="/latest",
    sort_routes=True,
    # default_version="v{major}",
).versionize()


# @TODO put CORS available/permissions in settings
origins = [
    "https://opennem.org.au",
    "https://dev.opennem.org.au",
    "https://staging.opennem.org.au",
    "https://admin.opennem.org.au",
    "https://admin.opennem.test",
    "http://localhost:8002",
    "http://127.0.0.1:8002",
    "https://admin.opennem.localhost",
    "https://*.opennem-fe.pages.dev",
    "https://*.pages.dev",
    "https://*.netlify.app",
    "https://*.openelectricity.org.au",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Process-Time", "X-ONAU", "X-ONAA"],
)


#  Maintenance mode middleware
@app.middleware("http")
async def intercept_maintenance_mode(request: Request, call_next):  # type: ignore
    if settings.maintenance_mode:
        logger.debug("Maintenance mode")

        resp_content = OpennemErrorSchema(error="Maintenance Mode")

        return OpennemExceptionResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, response_class=resp_content)

    response = await call_next(request)
    return response


# Custom exception handler
@app.exception_handler(OpennemBaseHttpException)
async def opennem_exception_handler(request: Request, exc: OpennemBaseHttpException) -> OpennemExceptionResponse:
    resp_content = OpennemErrorSchema(error=exc.detail)

    return OpennemExceptionResponse(
        status_code=exc.status_code,
        response_class=resp_content,
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> OpennemExceptionResponse:
    logger.debug(f"HTTP Exception: {exc.status_code} {exc.detail}")

    resp_content = OpennemErrorSchema(error=exc.detail, success=False)

    return OpennemExceptionResponse(
        status_code=exc.status_code,
        response_class=resp_content,
    )


@app.exception_handler(401)
@app.exception_handler(403)
async def http_type_exception_handler(request: Request, exc: HTTPException) -> OpennemExceptionResponse:
    resp_content = OpennemErrorSchema(error=exc.detail)

    return OpennemExceptionResponse(
        status_code=exc.status_code,
        response_class=resp_content,
    )


# setup caching
@app.on_event("startup")
async def startup() -> None:
    if settings.is_dev:
        logger.info("Cache disabled")
        FastAPICache.init(backend=InMemoryBackend())
        return None

    redis = aioredis.from_url(str(settings.redis_url), encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="api-cache")
    logger.info("Enabled API cache")


# sub-routers
app.include_router(stats_router, tags=["Stats"], prefix="/stats")
app.include_router(station_router, tags=["Stations"], prefix="/station")
app.include_router(facility_router, tags=["Facilities"], prefix="/facility")
app.include_router(weather_router, tags=["Weather"], prefix="/weather")
app.include_router(feedback_router, tags=["Feedback"], prefix="/feedback", include_in_schema=False)
app.include_router(dash_router, tags=["Dashboard"], prefix="/dash", include_in_schema=False)
app.include_router(milestones_router, tags=["Milestones"], prefix="/v4/milestones", include_in_schema=True)
app.include_router(webhooks_router, tags=["Webhooks"], prefix="/v4/webhooks", include_in_schema=False)


try:
    from fastapi.staticfiles import StaticFiles

    app.mount(
        "/static",
        StaticFiles(directory=settings.static_folder_path),
        name="static",
    )
except Exception as e:
    logger.info(f"Error initializing static hosting: {e}")


@app.get(
    "/robots.txt",
    response_class=FileResponse,
    include_in_schema=False,
)
def robots_txt() -> str:
    if not settings.debug:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return f"{settings.static_folder_path}/robots.txt"


@app.get(
    "/networks",
    response_model=list[APINetworkSchema],
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
)
def networks(
    session: Session = Depends(get_database_session),
) -> list[APINetworkSchema]:
    networks = session.query(Network).join(NetworkRegion, NetworkRegion.network_id == Network.code).all()

    if not networks:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return networks


@app.get(
    "/networks/regions",
    response_model=list[APINetworkRegion],
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
)
def network_regions(
    session: Session = Depends(get_database_session),
    network_code: str = Query(..., description="Network code"),
) -> list[APINetworkRegion]:
    network_id = network_code.upper()

    network_regions = session.query(NetworkRegion).filter_by(network_id=network_id).all()

    if not network_regions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    logger.debug(network_regions)

    response = [APINetworkRegion(code=i.code, timezone=i.timezone) for i in network_regions]

    return response


@app.get("/fueltechs", response_model=list[FueltechSchema])
def fueltechs(
    session: Session = Depends(get_database_session),
) -> list[FueltechSchema]:
    fueltechs = session.query(FuelTech).all()

    if not fueltechs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    try:
        models = [
            FueltechSchema(
                code=i.code,
                label=i.label,
                renewable=i.renewable,
            )
            for i in fueltechs
        ]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Invalid fueltechs") from e

    return models


@app.get("/intervals", response_model=list[TimeInterval])
def intervals() -> list[TimeInterval]:
    return INTERVALS


@app.get("/periods", response_model=list[TimePeriod])
def periods() -> list[TimePeriod]:
    return PERIODS


@app.get("/units", response_model=list[UnitDefinition])
def units() -> list[UnitDefinition]:
    return UNITS


@app.get("/health")
def health_check() -> str:
    """Health check"""
    return "OK"


@app.get("/protected", dependencies=[Depends(api_key_auth)])
def add_post() -> dict:
    return {"data": "You used a valid API key."}
