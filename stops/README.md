TransLink GTFS Stops GeoJSON
============================

`all_stops.geojson` is a GeoJSON FeatureCollection that
contains all of TransLink's stops.
It's derived from `stops.txt` in TransLink's GTFS Static Transit dataset.

Each stop is a Feature with a Point geometry.
Its properties include metadata about the stop.
For instance:

```
"properties": {
    "code": "55079",
    "desc": "123A ST @ 99 AVE",
    "id": "5131",
    "name": "SB 123A ST FS 99 AVE",
    "zone": "ZN 99"
}
```

Stops are sorted by their ID.
