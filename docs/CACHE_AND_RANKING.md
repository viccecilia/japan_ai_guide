# Cache Layer and Query Ranking

JAG-R011 adds an in-memory cache, a JSON-backed content index, query ranking, and a repository interface draft.

## Runtime Flow

```text
query
  -> intent
  -> token_gate
  -> content index
  -> query ranking
  -> cache lookup
  -> content repository / JSON loader
  -> answer_card_builder
  -> AnswerCard
  -> cache write
```

## Cache Layer

The cache lives in `backend/app/services/content_cache.py`. It is process-local memory only.

Current behavior:

- `get(key)` returns cached structured content when present and not expired.
- `set(key, value)` writes structured content after JSON load.
- `clear()` clears memory.
- `stats()` returns `hits`, `misses`, and `size`.

Service restart clears the cache. This is acceptable for this round.

## Cache Key Rules

Implemented in `backend/app/services/cache_key_builder.py`.

Format:

```text
intent_type:slug_or_entity_or_query:language
```

Examples:

```text
spot_query:kiyomizu:zh
food_query:kyoto_food:zh
generic_query:随便问一句:zh
```

Rules:

- Lowercase ASCII where applicable.
- Trim leading and trailing spaces.
- Collapse repeated spaces.
- Replace spaces with `_`.
- Prefer ranked slug.
- If slug is unavailable, fall back to `entity`, then `city`, then raw query.

## TTL Rules

Default TTL is 600 seconds. Expired entries are removed on lookup or stats collection.

## Content Index Rules

Implemented in `backend/app/services/content_index.py`.

The index is lazily built from JSON files under:

```text
backend/app/content_library/
```

Indexed fields:

- `slug`
- `title`
- `tags`
- `aliases`
- `language`
- `content_type`

Current supported content types:

- `spots`
- `foods`

The index structure also reserves folders for `cities`, `routes`, `culture`, and `hotels`.

## Query Ranking Rules

Implemented in `backend/app/services/query_ranking.py`.

Scores:

| Match rule | Score |
| --- | ---: |
| title exact match | 1.0 |
| alias exact match | 0.95 |
| query contains title | 0.9 |
| tag match | 0.75 |
| slug match | 0.7 |
| no match | 0 |

Output example:

```json
{
  "slug": "kiyomizu",
  "score": 1.0,
  "matched_by": "title"
}
```

## AnswerCard Metadata

Cache metadata:

```json
{
  "cache": {
    "hit": true,
    "key": "spot_query:kiyomizu:zh",
    "source": "memory",
    "ttl_seconds": 600
  }
}
```

Ranking metadata:

```json
{
  "ranking": {
    "slug": "kiyomizu",
    "score": 1.0,
    "matched_by": "title"
  }
}
```

## Repository Interface

`backend/app/services/content_repository.py` defines:

- `find_by_slug(slug, language, content_type)`
- `search(query, intent_type, language)`

The default implementation still delegates to JSON loaders.

## Why No Redis Or PostgreSQL In This Round

This round only establishes contracts and runtime behavior. Redis and PostgreSQL would add deployment and schema decisions that are premature before the AnswerCard content flow is stable.

## Future Migration

- Replace `InMemoryContentCache` with Redis using the same cache key builder.
- Replace JSON loader calls in `ContentRepository` with PostgreSQL queries.
- Keep AnswerCard Builder unchanged by preserving repository return types and metadata contracts.
