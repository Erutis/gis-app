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
# from geoalchemy2 import Geometry
# from sqlalchemy import Column, create_engine, text, insert
from sqlalchemy.orm import sessionmaker

# Internal libraries
from db_setup import Trajectory, engine_go_vroom


def main():
    """Enter sample data into Trajectory table."""
    engine = engine_go_vroom()
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create rows from sample data
    sample_data = [
        Trajectory(
            geom=f"SRID=4326;LINESTRINGZM({create_sample_linestring()})",
            feed_item_id=uuid.uuid4(),
        )
        for _ in range(2)
    ]

    session.add_all(sample_data)
    session.commit()


def create_sample_linestring():
    linestring = ""

    num_of_entries = int(random.uniform(0, 5))
    time = 0

    for n in range(num_of_entries):
        lat = round(random.uniform(30, 40), 3)
        lon = round(random.uniform(-70, -75), 3)
        alt = round(random.uniform(-1, 1), 2)
        time = time + int(random.uniform(0, 5))
        linestring += f"{lon} {lat} {alt} {time},"

    linestring = linestring[:-1]
    print(linestring[0:10])
    return linestring


if __name__ == "__main__":
    main()
