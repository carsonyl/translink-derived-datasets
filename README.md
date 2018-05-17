# TransLink derived datasets

These are transit-related GeoJSON datasets for Metro Vancouver,
derived from the [TransLink Open API](https://developer.translink.ca/) and
[GTFS Static Transit datasets](https://developer.translink.ca/ServicesGtfs/GtfsData).

These datasets are current as of **2018-05-06**.

As GeoJSON, these files can be previewed from within GitHub.
[Learn more](https://help.github.com/articles/mapping-geojson-files-on-github/).

## The datasets


### TransLink bus route pattern GeoJSON

Location: `datasets/route-patterns/`

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


### TransLink GTFS Shapes GeoJSON

Location: `datasets/shapes/`

This is a set of all of TransLink's GTFS Static Transit shapes in GeoJSON.
Shapes are grouped in folders by numeric shape ID divided by 100.

Each file is one GeoJSON Feature with a LineString geometry
and an `id` property.

Shape IDs are not directly meaningful.
They have an indirect relationship to routes via trip definitions.


### TransLink GTFS Stops GeoJSON

Location: `datasets/stops.geojson`

This is a GeoJSON FeatureCollection that
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


# Disclaimer

Route and arrival data used in this product or service is provided by
permission of TransLink. TransLink assumes no responsibility for the
accuracy or currency of the Data used in this product or service.


# Contact

File any issues at https://github.com/carsonyl/translink-derived-datasets/issues.

This is a project by Carson Lam - [@carsonyl](https://github.com/carsonyl).
