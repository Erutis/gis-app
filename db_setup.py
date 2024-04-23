#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By: K Agajanian

# Standard libraries
from datetime import datetime, timezone

import uuid

# External libraries

# Internal libraries

# Created: 2/21/24
# as of 3/6/24 this fucking works

# GeoAlchemy ORM Tutorial
# https://geoalchemy-2.readthedocs.io/en/latest/orm_tutorial.html

import docker
import logging
import os
import time
import traceback

from geoalchemy2 import Geometry
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    text,
    MetaData,
    Table,
    ForeignKey,
    DateTime,
    TIMESTAMP,
    UUID,
)

from sqlalchemy.orm import declarative_base, sessionmaker


ENV_VARS = {
    "MYDB__HOST": "localhost",
    "MYDB__DATABASE": "nyc",
    "POSTGRES_USER": "nyc",
    "MYDB__PORT": 5432,
    "MYDB__DRIVERNAME": "postgresql",
    "POSTGRES_PASSWORD": "gis",
    "platform": "linux/amd64",
}

LOCALHOST = ENV_VARS["MYDB__HOST"]
DB = ENV_VARS["MYDB__DATABASE"]
DRIVERNAME = ENV_VARS["MYDB__DRIVERNAME"]
USER = ENV_VARS["POSTGRES_USER"]
PW = ENV_VARS["POSTGRES_PASSWORD"]
PORT = ENV_VARS["MYDB__PORT"]


Base = declarative_base()


class Trajectory(Base):
    __tablename__ = "trajectory"
    id = Column(Integer, primary_key=True)
    create_time = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_time = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    geom = Column(Geometry("LINESTRINGZM"))
    feed_item_id = Column(UUID)


def setup_pg():
    """Create GIS engine, connect, and create tables."""
    url = f"{DRIVERNAME}://{USER}:{PW}@{LOCALHOST}:{PORT}/{DB}"
    engine = create_engine(url, echo=True)
    pg_check(engine=engine)

    # # Create Postgis extension & check that it works
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        conn.execute(text("SELECT postgis_full_version();"))

        Trajectory.__table__.create(engine)

        conn.commit()
        print("Committed!")

    return None


def pg_check(engine, max_retries=10):
    """Returns when the db is live."""

    for t in range(max_retries):
        try:
            time.sleep(5)
            with engine.connect():
                return True
        except Exception as exc:
            print("Oops that didn't work, lets try again!")
            print(exc)
            exc_ = exc
            time.sleep(5)

    raise exc_


# Still needs fixing
def insert_sample_data(engine):
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
    try:
        setup_pg()
        print("DB set up!")
        insert_sample_data()
        print("Sample data added!")
    except Exception as e:
        print(traceback.format_exc())
        print(e)
