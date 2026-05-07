import json
from dataclasses import dataclass, field
from pathlib import Path

from app.services.content_library_loader import CONTENT_LIBRARY_ROOT


@dataclass(frozen=True)
class ContentIndexItem:
    slug: str
    title: str
    aliases: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    content_type: str = "spot"
    language: str = "zh"
    priority: int = 50


_INDEX: list[ContentIndexItem] | None = None

CONTENT_FOLDERS = {
    "spots": "spot",
    "foods": "food",
    "cities": "city",
    "routes": "route",
    "culture": "culture",
    "hotels": "hotel",
}

KNOWN_ALIASES = {
    "kiyomizu": ["清水寺", "京都清水寺"],
    "fushimi_inari": ["伏见稻荷", "伏见稻荷大社"],
    "osaka_castle": ["大阪城"],
    "nara_park": ["奈良公园"],
    "kyoto_food": ["京都美食", "京都吃什么", "京都餐厅"],
}


def get_content_index() -> list[ContentIndexItem]:
    global _INDEX
    if _INDEX is None:
        _INDEX = build_content_index()
    return _INDEX


def build_content_index() -> list[ContentIndexItem]:
    items: list[ContentIndexItem] = []
    for folder, content_type in CONTENT_FOLDERS.items():
        folder_path = CONTENT_LIBRARY_ROOT / folder
        if not folder_path.exists():
            continue
        for path in sorted(folder_path.glob("*.json")):
            item = _read_index_item(path, content_type)
            if item is not None:
                items.append(item)
    return items


def _read_index_item(path: Path, folder_content_type: str) -> ContentIndexItem | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    slug = str(payload.get("slug") or path.stem)
    title = str(payload.get("title") or slug)
    aliases = [title, *[str(alias) for alias in payload.get("aliases", [])], *KNOWN_ALIASES.get(slug, [])]
    tags = [str(tag) for tag in payload.get("tags", [])]
    return ContentIndexItem(
        slug=slug,
        title=title,
        aliases=list(dict.fromkeys(aliases)),
        tags=tags,
        content_type=str(payload.get("content_type") or folder_content_type),
        language=str(payload.get("language") or "zh"),
        priority=int(payload.get("priority") or 50),
    )
