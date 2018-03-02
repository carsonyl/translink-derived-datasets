TransLink GTFS Shapes GeoJSON
=============================

This is a set of all of TransLink's GTFS Static Transit shapes in GeoJSON.
Shapes are grouped in folders by numeric shape ID divided by 100.

Each file is one GeoJSON Feature with a LineString geometry
and an `id` property.

Shape IDs are not directly meaningful.
They have an indirect relationship to routes via trip definitions.
