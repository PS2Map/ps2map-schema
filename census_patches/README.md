# Census Patch Data

These JSON files are meant to patch raw payloads received from the Census API - mostly to handle outdated or missing data.

When populating the database, a row whose primary field (e.g. `zone_id`) matches a key in the corresponding JSON (e.g. `census_patches/zone.json`) will be updated using `dict.update()`, overriding the original data.

To help differentiate these injected fields from the default ones, these keys are prefixed with `x-`.
