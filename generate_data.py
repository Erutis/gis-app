#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By: K Agajanian
# Created: 4/18/24

# Standard libraries
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

    # Generate sample data
    sample_data = [
        Trajectory(
            geom="SRID=4326;LINESTRINGZM(0 0 0 0, 1 1 1 1)",
            feed_item_id=uuid.uuid4(),
        )
        for _ in range(20)
    ]

    session.add_all(sample_data)
    session.commit()


if __name__ == "__main__":
    main()
