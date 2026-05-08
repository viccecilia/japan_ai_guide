# JAG-R021 Journey Storage Architecture

## Goal

R021 adds a Journey Persistence Protocol on top of active in-memory journey sessions.

```text
active journey session
-> save journey
-> saved journey record
-> restore journey
-> continue editing
-> delete journey
```

## Active Session vs Saved Record

Active journey session:

- current editing state
- in-memory
- identified by `session_id`
- changes during persona/pace/stop interactions

Saved journey record:

- snapshot of editable itinerary
- has stable `journey_id`
- includes interaction history, analytics, and replay
- has `created_at`, `updated_at`, and `status`

## Current Storage

R021 uses in-memory storage only:

- no PostgreSQL
- no Redis
- no real user account
- no login

## Restore Flow

Restore loads a saved journey record back into the active journey session so editing can continue.

## Delete Flow

Delete marks a saved record as `deleted` and removes it from the list API.

## Future PostgreSQL

The storage schema is ready to map to a `saved_journeys` table in a future round.

## Future User Account

`user_id` is present as a future field, but R021 does not implement OAuth, WeChat login, Google login, or any real account system.

## Future Redis Cache

Redis can later hold active sessions while PostgreSQL persists saved records.
