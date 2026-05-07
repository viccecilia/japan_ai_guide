# Content Repository Expansion

JAG-R012 expands the Content Repository from single best slug ranking to top-k candidate ranking.

## Content Types

The unified Content Library now supports:

- `spot`
- `city`
- `food`
- `route`
- `culture`
- `hotel`

Seed folders:

```text
backend/app/content_library/
├─ spots/
├─ cities/
├─ foods/
├─ routes/
├─ culture/
└─ hotels/
```

## Expanded Content Fields

Content seed files now support:

- `content_type`
- `aliases`
- `priority`
- `updated_at`

These fields are indexed by `backend/app/services/content_index.py`.

## Top-K Ranking

`backend/app/services/query_ranking.py` exposes:

```python
rank_top_k(query, intent, index, top_k=5)
```

Each result includes:

```json
{
  "slug": "kiyomizu",
  "score": 1.0,
  "matched_by": "title",
  "content_type": "spot",
  "priority": 90
}
```

The resolver uses the first candidate as the primary AnswerCard source and writes the remaining candidates into metadata.

## related_candidates

AnswerCard metadata now includes:

```json
{
  "related_candidates": [
    {
      "slug": "kyoto_city",
      "score": 0.75,
      "matched_by": "tag",
      "content_type": "city",
      "priority": 95
    }
  ]
}
```

This is development metadata for future recommendation, multi-card rendering, and PostgreSQL search tuning.

## Aliases

Aliases let a query match user wording that differs from the official title. For example:

```json
{
  "title": "京都站周边住宿",
  "aliases": ["京都住宿", "京都酒店", "京都站酒店"]
}
```

## Priority

Priority is used as a tie-breaker when ranking scores are equal. Higher priority appears earlier.

## Repository Abstraction

`backend/app/services/content_repository.py` now exposes:

- `find_by_slug(slug, language, content_type)`
- `search(query, intent_type, language)`
- `search_candidates(query, intent_type, language, top_k=5)`

The implementation still reads JSON through the loader.

## Future PostgreSQL Migration

The future PostgreSQL repository can preserve the same interface and replace:

- JSON file scan with SQL index lookup
- alias/tag matching with indexed columns or `pg_trgm`
- priority with ranking weights
- language with a composite key on `slug + language`

AnswerCard Builder should not need to change if repository return types stay stable.
