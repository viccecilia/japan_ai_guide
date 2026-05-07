import json
from pathlib import Path
from typing import TypeVar

from pydantic import ValidationError

from app.schemas.content_library import (
    CityContent,
    CultureContent,
    FoodContent,
    HotelContent,
    RouteContent,
    SpotContent,
)


ContentModel = TypeVar("ContentModel", CityContent, CultureContent, FoodContent, HotelContent, RouteContent, SpotContent)

CONTENT_LIBRARY_ROOT = Path(__file__).resolve().parents[1] / "content_library"


def load_spot_content(slug: str, language: str = "zh") -> SpotContent | None:
    return _load_content("spots", slug, SpotContent, language)


def load_city_content(slug: str, language: str = "zh") -> CityContent | None:
    return _load_content("cities", slug, CityContent, language)


def load_food_content(slug: str, language: str = "zh") -> FoodContent | None:
    return _load_content("foods", slug, FoodContent, language)


def load_route_content(slug: str, language: str = "zh") -> RouteContent | None:
    return _load_content("routes", slug, RouteContent, language)


def load_culture_content(slug: str, language: str = "zh") -> CultureContent | None:
    return _load_content("culture", slug, CultureContent, language)


def load_hotel_content(slug: str, language: str = "zh") -> HotelContent | None:
    return _load_content("hotels", slug, HotelContent, language)


def _load_content(
    folder: str,
    slug: str,
    model: type[ContentModel],
    language: str,
) -> ContentModel | None:
    safe_slug = slug.strip().lower()
    if not safe_slug:
        return None

    path = CONTENT_LIBRARY_ROOT / folder / f"{safe_slug}.json"
    if not path.exists():
        return None

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        content = model.model_validate(payload)
    except (json.JSONDecodeError, OSError, ValidationError):
        return None

    if content.language != language:
        return None
    return content
