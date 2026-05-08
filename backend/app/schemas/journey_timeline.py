from pydantic import BaseModel, Field

from app.schemas.itinerary import ItineraryStop


class JourneyBlock(BaseModel):
    block_type: str = "activity"
    title: str
    time_of_day: str = "daytime"
    stops: list[ItineraryStop] = Field(default_factory=list)
    narrative: str | None = None


class JourneyTransition(BaseModel):
    from_city: str
    to_city: str
    recommended_transport: str = "JR / 新干线"
    estimated_travel_time: str = "约1-3小时"
    estimated_transition_time: str = "约1-3小时"
    transition_type: str = "rail"
    transition_load: str = "normal"
    narrative: str


class JourneyDay(BaseModel):
    day_number: int
    title: str
    city: str
    date_label: str | None = None
    blocks: list[JourneyBlock] = Field(default_factory=list)
    hotel: ItineraryStop | None = None
    daily_narrative: str
    pace: str = "normal"


class JourneyTimeline(BaseModel):
    timeline_id: str
    title: str
    days: list[JourneyDay] = Field(default_factory=list)
    cities: list[str] = Field(default_factory=list)
    hotels: list[ItineraryStop] = Field(default_factory=list)
    transitions: list[JourneyTransition] = Field(default_factory=list)
    total_duration: str = "1-day"
    journey_style: str = "classic"
