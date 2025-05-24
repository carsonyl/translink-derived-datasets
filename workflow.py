import os
import shutil
import subprocess
from csv import DictReader, DictWriter
from datetime import date, timedelta
from itertools import groupby
from tempfile import TemporaryFile
from zipfile import ZipFile

import click
import geojson
from geojson import Point, Feature, FeatureCollection, LineString
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


session = Session()
adapter = HTTPAdapter(
    max_retries=Retry(
        total=5,
        connect=5,
        read=5,
        backoff_factor=0.3,
    )
)
session.mount("http://", adapter)
session.mount("https://", adapter)


def open_bom(path):
    return open(path, encoding="utf-8-sig")


def gtfs_rows(filename):
    with open_bom(os.path.join("gtfs", filename)) as inf:
        for row in DictReader(inf):
            yield {k: v.strip() for k, v in row.items()}


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "--url",
    default=lambda: os.environ.get("GTFS_URL"),
    show_default="from GTFS_URL env var",
)
def gtfs(url):
    """Download the latest GTFS dataset and extract routes, shapes, and stops."""
    if not url:
        raise click.UsageError("GTFS_URL is not set.")
    with TemporaryFile() as outf:
        with session.get(url, stream=True) as dl:
            dl.raise_for_status()
            for chunk in dl.iter_content(1024):
                outf.write(chunk)
        with ZipFile(outf) as zipf:
            for f in ["routes.txt", "shapes.txt", "stops.txt"]:
                dest_txt = os.path.join("gtfs", f)
                if os.path.exists(dest_txt):
                    os.remove(dest_txt)
                zipf.extract(f, "gtfs")
                dest_csv = os.path.join("gtfs", f.replace(".txt", ".csv"))
                if os.path.exists(dest_csv):
                    os.remove(dest_csv)
                os.rename(dest_txt, dest_csv)


def coord_for_row(shape_row):
    return float(shape_row["shape_pt_lon"]), float(shape_row["shape_pt_lat"])


def make_linestring(shape_rows):
    return LineString(
        [
            coord_for_row(row)
            for row in sorted(shape_rows, key=lambda row: int(row["shape_pt_sequence"]))
        ]
    )


@cli.command()
def shapes():
    """Write a GeoJSON file for each Shape."""
    # Remove all subdirectories in the output directory.
    root_dir = os.path.join("datasets", "shapes")
    if os.path.exists(root_dir):
        shutil.rmtree(root_dir)

    # This assumes the GTFS shapes are presorted.
    for shape_id, rows in groupby(gtfs_rows("shapes.csv"), lambda row: row["shape_id"]):
        print(f"Working on {shape_id}")
        feature = Feature(
            id=shape_id,
            geometry=make_linestring(rows),
            properties={
                "id": shape_id,
                "stroke-width": 3.0,
            },
        )

        dest_dir = os.path.join(root_dir, str(int(shape_id) // 100 * 100))
        try:
            os.makedirs(dest_dir)
        except FileExistsError:
            pass

        with open(os.path.join(dest_dir, f"{shape_id}.geojson"), "w") as outf:
            outf.write(geojson.dumps(feature, sort_keys=True, indent=1))


def gtfs_route_numbers():
    return sorted(
        {route["route_short_name"].strip() for route in gtfs_rows("routes.csv")}
    )


def stop_to_feature(stop):
    point = Point((float(stop["stop_lon"]), float(stop["stop_lat"])))
    return Feature(
        id=stop["stop_id"],
        geometry=point,
        properties={
            "id": stop["stop_id"],
            "name": stop["stop_name"],
            "desc": stop["stop_desc"],
            "code": stop["stop_code"].strip(),
            "zone": stop.get("zone_id"),
            "wheelchair_boarding": stop.get("wheelchair_boarding"),
        },
    )


@cli.command()
def stops():
    """Write a GeoJSON file containing all stops."""
    dest_dir = "datasets"
    try:
        os.makedirs(dest_dir)
    except FileExistsError:
        pass

    stops = sorted(gtfs_rows("stops.csv"), key=lambda stop: int(stop["stop_id"]))
    print(f"{len(stops)} stops")
    coll = FeatureCollection([stop_to_feature(stop) for stop in stops])

    with open(os.path.join(dest_dir, "stops.geojson"), "w") as outf:
        outf.write(geojson.dumps(coll, sort_keys=True, indent=1))

    fields = "stop_id,stop_code,stop_name,stop_desc,stop_lat,stop_lon,zone_id,stop_url,location_type,parent_station,wheelchair_boarding,stop_timezone"
    fields = fields.split(",")

    with open(os.path.join(dest_dir, "stops.csv"), "w", newline="") as outf:
        writer = DictWriter(outf, fields)
        writer.writeheader()
        writer.writerows(stops)


@cli.command()
def git():
    last_friday = date.today() + timedelta(days=4 - date.today().weekday())
    commands = [
        ["git", "add", "datasets/stops*"],
        ["git", "commit", "-m", f"Stops {last_friday.isoformat()}."],
        ["git", "add", "datasets/shapes"],
        ["git", "commit", "-m", f"Shapes {last_friday.isoformat()}."],
    ]
    for cmd in commands:
        print(">>> " + " ".join(cmd))
        subprocess.run(cmd)


@cli.command()
@click.pass_context
def changes(ctx):
    ctx.invoke(gtfs)
    ctx.invoke(stops)
    ctx.invoke(shapes)


if __name__ == "__main__":
    cli()
