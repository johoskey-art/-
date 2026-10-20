# Minimal portable MASTER format (version 0.1)

JSON object:
- `schema_version`: "0.1"
- `industry`: readable label
- `scope`: object `{ "exclude_company_ids": ["KR:000000"] }`; all other scope boundaries still documented in metadata or a dedicated local scope file
- `companies`: array of `{id, name, market, ticker, role, products, source_ids, home_group_ids}`; `role` CORE / STRUCTURAL / OPTION / SIGNAL and `products` is a list of sellable product names
- `groups`: array of `{id, name, kind:"HOME", companies:[ids], description, profit_driver}`
- `events`: array of `{id, title, companies:[ids], category, profit_bridge:[...], next_indicator, confirmatory, contradictory}`
- `sources`: array `{id, type, title, as_of, uri?}`

This is a *starter* schema, not a substitute for full product-level claims. For production, expand into company×product claims, evidence links, source timestamps, actual versus forecast distinctions and business-specific role ratings. Do not guess financial metrics to satisfy a schema.
