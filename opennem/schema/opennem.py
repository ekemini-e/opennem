# pylint: disable=no-name-in-module
# pylint: disable=no-self-argument
# pylint: disable=no-member
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from geoalchemy2.elements import WKBElement
from geoalchemy2.shape import to_shape
from pydantic import BaseModel, ValidationError, validator
from shapely import geometry

from opennem.api.photo.schema import Photo
from opennem.api.stats.schema import OpennemData
from opennem.api.weather.schema import WeatherStation
from opennem.core.dispatch_type import DispatchType
from opennem.core.networks import datetime_add_network_timezone
from opennem.core.normalizers import clean_capacity, normalize_string
from opennem.utils.version import __VERSION__

from .core import BaseConfig
from .network import NetworkNEM, NetworkSchema


class ResponseStatus(Enum):
    OK = "OK"
    ERROR = "ERROR"


class OpennemBaseSchema(BaseConfig):
    version: str = __VERSION__
    response_status: ResponseStatus = ResponseStatus.OK


class FueltechSchema(BaseConfig):
    code: str
    label: Optional[str]
    renewable: Optional[bool]


class FacilityStatusSchema(BaseConfig):
    code: str
    label: Optional[str]


class ParticipantSchema(OpennemBaseSchema):
    id: int
    code: Optional[str]
    name: str
    network_name: Optional[str] = None
    network_code: Optional[str] = None
    country: Optional[str] = None
    abn: Optional[str] = None


class StationBaseSchema(OpennemBaseSchema):
    id: int


class FacilityBaseSchema(OpennemBaseSchema):
    id: int


class GeoPoint(BaseModel):
    lat: float
    lng: float


class GeoBoundary(BaseModel):
    pass


class RecordTypes(str, Enum):
    station = "station"
    facility = "facility"
    location = "location"
    revision = "revision"


class RevisionSchema(OpennemBaseSchema):
    id: int

    changes: Dict[str, Union[str, int, float, bool, None]] = {}
    previous: Optional[Dict[str, Union[str, int, float, bool]]] = {}

    parent_id: Optional[int]
    parent_type: Optional[str]
    station_owner_id: Optional[int]
    station_owner_name: Optional[str]
    station_owner_code: Optional[str]

    is_update: bool = False

    approved: bool = False
    approved_by: Optional[str]
    approved_at: Optional[datetime]
    approved_comment: Optional[str]

    discarded: bool = False
    discarded_by: Optional[str]
    discarded_at: Optional[datetime]


class ScadaReading(Tuple[datetime, Optional[float]]):
    pass


class FacilitySchema(OpennemBaseSchema):
    id: Optional[int]

    network: NetworkSchema = NetworkNEM

    fueltech: Optional[FueltechSchema]

    status: Optional[FacilityStatusSchema]

    station_id: Optional[int]

    # @TODO no longer optional
    code: Optional[str] = ""

    scada_power: Optional[OpennemData]

    dispatch_type: DispatchType = DispatchType.GENERATOR

    active: bool = True

    capacity_registered: Optional[float]

    registered: Optional[datetime]
    deregistered: Optional[datetime]

    network_region: Optional[str]

    unit_id: Optional[int]
    unit_number: Optional[int]
    unit_alias: Optional[str]
    unit_capacity: Optional[float]

    emissions_factor_co2: Optional[float]

    approved: bool = False
    approved_by: Optional[str]
    approved_at: Optional[datetime]

    @validator("capacity_registered")
    def _clean_capacity_regisered(cls, value: Union[str, int, float]) -> Optional[float]:
        _v = clean_capacity(value)

        if isinstance(value, float):
            _v = round(value, 2)

        return _v

    @validator("emissions_factor_co2")
    def _clean_emissions_factor_co2(cls, value: Union[str, int, float]) -> Optional[float]:
        _v = clean_capacity(value)

        return _v


class WeatherStationNearest(BaseModel):
    code: str
    distance: float


class LocationSchema(OpennemBaseSchema):
    id: Optional[int]

    weather_station: Optional[WeatherStation]
    weather_nearest: Optional[WeatherStationNearest]

    address1: Optional[str] = ""
    address2: Optional[str] = ""
    locality: Optional[str] = ""
    state: Optional[str] = ""
    postcode: Optional[str] = ""
    country: Optional[str] = "au"

    # Geo fields
    # place_id: Optional[str]
    geocode_approved: bool = False
    geocode_skip: bool = False
    geocode_processed_at: Optional[datetime] = None
    geocode_by: Optional[str]
    geom: Optional[Any] = None
    boundary: Optional[Any]

    lat: Optional[float]
    lng: Optional[float]

    @validator("address1")
    def clean_address(cls, value: str) -> str:
        return normalize_string(value)

    @validator("address2")
    def clean_address2(cls, value: str) -> str:
        return normalize_string(value)

    @validator("locality")
    def clean_locality(cls, value: str) -> str:
        return normalize_string(value)

    @validator("state")
    def state_upper(cls, value: str) -> Optional[str]:
        if value:
            return value.upper()

        return None

    @validator("postcode")
    def clean_postcode(cls, value: str) -> Optional[str]:
        if value:
            return value.strip()

        return None

    @validator("geom", pre=True)
    def parse_geom(cls, value: WKBElement) -> Any:

        if value:
            return geometry.mapping(to_shape(value))

    @validator("boundary", pre=True)
    def parse_boundary(cls, value: WKBElement) -> Any:

        if value:
            return geometry.mapping(to_shape(value))


def as_nem_timezone(dt: datetime) -> datetime:
    if dt:
        return datetime_add_network_timezone(dt, NetworkNEM)

    raise Exception("Require a date for nem timezone")


def _flatten_linked_object(value: Union[str, Dict, object]) -> str:
    if isinstance(value, str):
        return value

    if isinstance(value, dict) and "code" in value:
        return value["code"]

    if isinstance(value, object) and hasattr(value, "code"):
        return value.code  # type: ignore

    raise ValidationError("Could not flatten no value or invalid", model=StationSchema)


class FacilityOutputSchema(OpennemBaseSchema):
    id: Optional[int]

    network: str = "NEM"

    fueltech: Optional[str]

    status: Optional[str]

    # @TODO no longer optional
    code: Optional[str] = ""

    scada_power: Optional[OpennemData]

    dispatch_type: DispatchType = DispatchType.GENERATOR

    capacity_registered: Optional[float]

    registered: Optional[datetime]
    deregistered: Optional[datetime]

    network_region: Optional[str]

    unit_id: Optional[int]
    unit_number: Optional[int]
    unit_alias: Optional[str]
    unit_capacity: Optional[float]

    emissions_factor_co2: Optional[float]

    data_first_seen: Optional[datetime]
    data_last_seen: Optional[datetime]

    _seen_dates_tz = validator("data_first_seen", "data_last_seen", pre=True, allow_reuse=True)(
        as_nem_timezone
    )

    _flatten_embedded = validator("network", "fueltech", "status", pre=True, allow_reuse=True)(
        _flatten_linked_object
    )

    @validator("capacity_registered")
    def _clean_capacity_regisered(cls, value: Union[str, float, int]) -> Optional[float]:
        _v = clean_capacity(value)

        if isinstance(value, float):
            _v = round(value, 2)

        return _v

    @validator("emissions_factor_co2")
    def _clean_emissions_factor_co2(cls, value: Union[str, float, int]) -> Optional[float]:
        _v = clean_capacity(value)

        return _v


class FacilityImportSchema(OpennemBaseSchema):
    id: Optional[int]

    network: NetworkSchema = NetworkNEM
    network_id: Optional[str]

    fueltech: Optional[FueltechSchema]
    fueltech_id: Optional[str]

    status: Optional[FacilityStatusSchema]
    status_id: Optional[str]

    # @TODO no longer optional
    code: Optional[str] = ""

    scada_power: Optional[OpennemData]

    dispatch_type: DispatchType = DispatchType.GENERATOR

    active: bool = True

    capacity_registered: Optional[float]

    registered: Optional[datetime]
    deregistered: Optional[datetime]

    network_region: Optional[str]

    unit_id: Optional[int]
    unit_number: Optional[int]
    unit_alias: Optional[str]
    unit_capacity: Optional[float]

    emissions_factor_co2: Optional[float]

    approved: bool = False
    approved_by: Optional[str]
    approved_at: Optional[datetime]


class StationImportSchema(OpennemBaseSchema):
    id: Optional[int]

    code: str

    participant: Optional[ParticipantSchema] = None

    facilities: Optional[List[FacilityImportSchema]] = []

    photos: Optional[List[Photo]]

    name: Optional[str]

    # Original network fields
    network_name: Optional[str]

    location: LocationSchema = LocationSchema()

    network: Optional[str] = None

    approved: bool = True

    description: Optional[str]
    wikipedia_link: Optional[str]
    wikidata_id: Optional[str]
    website_url: Optional[str]


class StationSchema(OpennemBaseSchema):
    id: Optional[int]

    code: str

    participant: Optional[ParticipantSchema] = None

    facilities: Optional[List[FacilitySchema]] = []

    photos: Optional[List[Photo]]

    name: Optional[str]

    # Original network fields
    network_name: Optional[str]

    location: LocationSchema = LocationSchema()

    network: Optional[str] = None

    approved: bool = True

    data_first_seen: datetime
    data_last_seen: datetime

    description: Optional[str]
    wikipedia_link: Optional[str]
    wikidata_id: Optional[str]
    website_url: Optional[str]


class StationOutputSchema(OpennemBaseSchema):
    id: Optional[int]

    code: str

    participant: Optional[ParticipantSchema] = None

    facilities: Optional[List[FacilityOutputSchema]] = []

    photos: Optional[List[Photo]]

    name: Optional[str]

    # Original network fields
    network_name: Optional[str]

    location: LocationSchema = LocationSchema()

    network: Optional[str] = None

    description: Optional[str]
    wikipedia_link: Optional[str]
    wikidata_id: Optional[str]
    website_url: Optional[str]
