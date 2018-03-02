TransLink bus route pattern GeoJSON
===================================

These are the patterns for TransLink bus routes, in GeoJSON format.
A pattern is a distinct path taken by a bus route.
The GeoJSON files can be previewed in the GitHub interface.

Patterns are grouped by route number.
Filenames are of the form `[route number]-[direction]-[pattern number].geojson`.
If a pattern exists but its geometry is not available,
the filename will end in `.missing` instead.

Each GeoJSON file contains a single Feature.
Its properties include metadata about the route and pattern.
For instance:

```
"properties": {
    "destination": "SFU",
    "direction": "NORTH",
    "name": "144-NB1",
    "operating-company": "CMBC",
    "pattern-number": "NB1",
    "route-name": "SFU/METROTOWN STN",
    "route-number": "144",
    "stroke": "#267cff",
    "stroke-width": 3.0
}
```

This dataset comes from the TransLink Open API.
Pattern geometry originates from KMZ.
