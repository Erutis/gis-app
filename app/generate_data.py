#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By: K Agajanian
# Created: 4/18/24

# Standard libraries
import random
import uuid

# from datetime import datetime

# External libraries
from sqlalchemy.orm import sessionmaker

# Internal libraries
from db_setup import Trajectory, engine_go_vroom


# Pre-determined areas for random data generation
central_park = {"lon": (-73.973, -73.958), "lat": (40.765, 40.800)}
northeast = {"lon": (-70, -75), "lat": (40, 43)}


def main():
    """Enter sample data into Trajectory table."""
    engine = engine_go_vroom()
    Session = sessionmaker(bind=engine)
    session = Session()

    for _ in range(5):
        try:
            # Create rows from sample data
            sample_data = [
                Trajectory(
                    geom=f"SRID=4326;LINESTRINGZM({create_sample_linestring(central_park)})",
                    feed_item_id=uuid.uuid4(),
                )
            ]

            session.add_all(sample_data)
            session.commit()

        except Exception as e:
            print(e)
            continue


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

        # Linestring hates being alone and I don't wanna deal with POINTs
        if num_of_entries <= 1:
            linestring += linestring

    linestring = linestring[:-1]
    print(f"HERE'S MY LINESTRING BETCH: {linestring}")
    return linestring


if __name__ == "__main__":
    main()
