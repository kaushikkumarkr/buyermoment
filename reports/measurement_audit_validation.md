# Measurement audit validation

The local audit distinguishes `TRACKING_READY`, `TRACKING_PARTIAL`, and `TRACKING_UNSAFE`.

Validated failure conditions include missing primary conversion, missing UTMs, and disabled deduplication. Validated ready conditions require primary conversion, UTMs, deduplication, CRM linkage, offline conversion path, pipeline/revenue fields, and conversion lag. Missing data remains missing; no economic value is fabricated.
