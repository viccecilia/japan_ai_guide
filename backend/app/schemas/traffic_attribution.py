from pydantic import BaseModel


class TrafficAttribution(BaseModel):
    utm_source: str | None = None
    utm_campaign: str | None = None
    referrer: str | None = None
    landing_page: str | None = None
    device: str = "unknown"
    language: str = "zh"
    country: str | None = None
