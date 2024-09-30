#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By: K Agajanian
# Created: 4/18/24

# Standard libraries
import json
import os
import random
import sys
import uuid

# External libraries
from sqlalchemy import create_engine, select, func, update
from sqlalchemy.orm import sessionmaker


# Add the parent directory to the Python path
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Internal libraries
from app.tables import Trajectory, FeedItem


# Pre-determined areas for random data generation
central_park = {"lon": (-73.973, -73.958), "lat": (40.765, 40.800)}
northeast = {"lon": (-70, -75), "lat": (40, 43)}

url = os.getenv("DATABASE_URL")
engine = create_engine(url)

Session = sessionmaker(bind=engine)
session = Session()


def add_db_rows():
    """Enter sample data into Trajectory table."""

    sample_data = []

    try:
        for _ in range(5):
            # Create rows from sample data
            linestring, geom_type = create_sample_linestring(central_park)

            feed_item = FeedItem(id=uuid.uuid4(), name="hurhur")

            trajectory = Trajectory(
                geom=f"SRID=4326;{geom_type}({linestring})",
                feed_item_id=feed_item.id,
            )

            sample_data.append(trajectory)
            sample_data.append(feed_item)

        session.add_all(sample_data)
        session.commit()

    except Exception as e:
        print(e)


def create_sample_linestring(area):
    linestring = ""

    num_of_entries = int(random.uniform(1, 5))  # must have at least 2
    time = 0

    for n in range(num_of_entries):
        lon = round(random.uniform(area["lon"][0], area["lon"][1]), 3)  # x coordinate
        lat = round(random.uniform(area["lat"][0], area["lat"][1]), 3)  # y coordinate
        alt = round(random.uniform(-1, 1), 0)  # altitude
        time = time + int(random.uniform(0, 5))  # time
        linestring += f"{lon} {lat} {alt} {time},"

        # If only one item in linestring, geom_type is a POINT, else LINESTRING
        if num_of_entries <= 1:
            geom_type = "POINTZM"
        else:
            geom_type = "LINESTRINGZM"

    # Remove trailing comma at end of string
    linestring = linestring[:-1]

    return linestring, geom_type


def retrieve_row():
    """Retrieve recently created row."""
    q = select(Trajectory)
    with session as s:
        trajs = s.execute(q).scalars().all()

    print(f"Retrieved feed item: {[traj.id for traj in trajs]}")


def append_trajectory(traj_id, traj_to_append):
    """Pull the database record as a GeoJSON. Update the coordinates by appending.
    Pull the ORM object. Replace the contents of the geometry column. Commit.
    !!!! Problem: ST_AsGeoJSON doesn't support 4-dimensional records. Only 3 are pulled.
    """
    q = select(func.ST_AsGeoJSON(Trajectory))
    q = q.where(Trajectory.id == traj_id)
    with session as s:
        traj = s.execute(q).one_or_none()

    traj = json.loads(traj[0])

    traj["geometry"]["coordinates"].append(traj_to_append)
    new_coords = traj["geometry"]["coordinates"]
    geom_type = traj["geometry"]["type"]

    q = select(Trajectory).where(Trajectory.id == traj_id)
    with session as s:
        traj = s.execute(q).scalars().one_or_none()

    traj.geom = f"SRID=4326;{geom_type}({new_coords})"


def update_traj(traj_id, traj_to_append):
    # if needed, stringify
    # traj_to_append = f"{str(traj_to_append)[1:-1]}"
    len_of_traj = len(traj_to_append)  # for later
    traj_to_append = func.ST_MakePoint(
        traj_to_append[0], traj_to_append[1], traj_to_append[2]
    )
    q = update(Trajectory).where(Trajectory.id == traj_id)
    q = q.values(geom=func.ST_AddPoint(Trajectory.geom, traj_to_append))

    session.execute(q)
    session.commit()


if __name__ == "__main__":
    add_db_rows()
    retrieve_row()
    print("DB commit successful.")
