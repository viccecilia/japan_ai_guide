# Content Library Query Layer

JAG-R010 introduces the first structured content layer for Japan AI Guide. The runtime path is:

```text
User Query
  -> Intent Router
  -> Token Gate
  -> Content Resolver
  -> AnswerCard Builder
  -> AnswerCard Response
```

This round does not connect a database, realtime AI, map, TTS, or charter booking. JSON files are the current source of truth.

## Directory Structure

```text
backend/app/content_library/
├─ spots/
│  ├─ kiyomizu.json
│  ├─ fushimi_inari.json
│  ├─ osaka_castle.json
│  └─ nara_park.json
├─ cities/
├─ foods/
│  └─ kyoto_food.json
├─ routes/
├─ culture/
└─ hotels/
```

## JSON Format

Each content file follows the shared schema in `backend/app/schemas/content_library.py`.

```json
{
  "id": "spot_kiyomizu",
  "slug": "kiyomizu",
  "title": "清水寺",
  "subtitle": "京都 · 东山区",
  "description": "适合第一次了解清水寺的基础讲解。",
  "story": "用于 AnswerCard 主体故事讲解。",
  "tags": ["京都", "寺院"],
  "nearby": [],
  "foods": [],
  "hotels": [],
  "source": "content_library",
  "language": "zh"
}
```

## Slug Rules

- Use lowercase ASCII.
- Use `_` between words, for example `fushimi_inari`.
- File name must equal slug, for example `kiyomizu.json`.
- Slug is stable and must not be translated.

## Language Rules

- Current seed language is `zh`.
- The loader only returns content when `content.language` matches the request language.
- Future multilingual content should use one file per slug per language or a database table keyed by `slug + language`.

## Fallback Rules

If the resolver cannot find content, the Builder returns a template AnswerCard. The user still receives a normal card.

Content Library metadata:

```json
{
  "content_source": {
    "type": "content_library",
    "slug": "kiyomizu",
    "language": "zh"
  }
}
```

Template fallback metadata:

```json
{
  "content_source": {
    "type": "template"
  }
}
```

## Token Gate Relationship

Token Gate still runs before the Builder. In JAG-R010, realtime AI remains disabled by default. Content Library is the preferred low-cost layer before any future realtime AI generation.

## Future Database Relationship

The JSON loader should later be replaced by a repository layer backed by PostgreSQL. The current `slug`, `language`, and structured fields are designed to map directly to database columns or JSONB fields.
