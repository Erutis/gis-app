#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By: K Agajanian
# Created: 4/18/24

# Standard libraries
from datetime import datetime

# External libraries
from geoalchemy2 import Geometry
from sqlalchemy import Column, create_engine, text, insert

# Internal libraries
from db_setup import Trajectory, DRIVERNAME, USER, PW, LOCALHOST, PORT, DB


def create_new_data():
    # connect to engine
    url = f"{DRIVERNAME}://{USER}:{PW}@{LOCALHOST}:{PORT}/{DB}"
    engine = create_engine(url, echo=True)

    with engine.connect() as conn:
        stmt = insert(Trajectory).values(
            id=1234,
        )


def main():
    pass


if __name__ == "__main__":
    main()
