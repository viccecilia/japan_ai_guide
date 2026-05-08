from pydantic import BaseModel, Field


class ItineraryStop(BaseModel):
    title: str
    subtitle: str | None = None
    stop_type: str = "spot"
    estimated_time: str | None = None
    transport_notes: str | None = None
    narrative: str | None = None


class ItineraryBlock(BaseModel):
    block_title: str
    time_of_day: str
    stops: list[ItineraryStop] = Field(default_factory=list)
    narrative: str | None = None


class Itinerary(BaseModel):
    title: str
    city: str | None = None
    duration: str = "half_day"
    route_type: str = "classic"
    persona: str | None = None
    persona_label: str | None = None
    pace: str | None = None
    journey_style: str | None = None
    stops: list[ItineraryStop] = Field(default_factory=list)
    foods: list[ItineraryStop] = Field(default_factory=list)
    culture: list[ItineraryStop] = Field(default_factory=list)
    hotel: ItineraryStop | None = None
    blocks: list[ItineraryBlock] = Field(default_factory=list)
    transport_notes: str | None = None
    estimated_time: str | None = None
    narrative: str | None = None


class TravelFlow(BaseModel):
    flow_type: str
    title: str
    summary: str
    persona: str | None = None
    pace: str | None = None
    journey_style: str | None = None
    itineraries: list[Itinerary] = Field(default_factory=list)
    journey_prompts: list[str] = Field(default_factory=list)
