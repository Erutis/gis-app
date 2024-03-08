#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By: K Agajanian

# Standard libraries

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
    "MYDB__DATABASE": "gis",
    "POSTGRES_USER": "gis",
    "MYDB__PORT": "gis",
    "MYDB__DRIVERNAME": "postgresql",
    "POSTGRES_PASSWORD": "gis",
    "platform": "linux/amd64",
}


def setup_pg():
    localhost = ENV_VARS["MYDB__HOST"]
    db = ENV_VARS["MYDB__DATABASE"]
    drivername = ENV_VARS["MYDB__DRIVERNAME"]
    user = ENV_VARS["POSTGRES_USER"]
    pw = ENV_VARS["POSTGRES_PASSWORD"]

    engine = create_engine(f"postgresql://gis:gis@localhost:5432/gis", echo=True)
    pg_check(engine=engine)

    # # Create Postgis extension
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))

    return None


def create_tables():
    engine = create_engine("postgresql://gis:gis@localhost:5432/gis", echo=True)
    Base = declarative_base()

    with engine.connect() as conn:

        class Trajectory(Base):
            __tablename__ = "nyc"
            id = Column(Integer, primary_key=True)
            create_time = Column(TIMESTAMP)
            updated_time = Column(TIMESTAMP)
            geom = Column(Geometry("LINESTRINGZM"))
            feed_item_id = Column(UUID)

        # Trajectory.__table__
        Trajectory.__table__.create(engine)
        conn.commit()


def pg_check(engine, max_retries=10):
    """Returns when the db is live."""

    for t in range(max_retries):
        try:
            time.sleep(5)
            with engine.connect():
                return True
        except Exception as exc:
            print("Oops that didn't work, lets try again! ")
            print(exc)
            exc_ = exc
            time.sleep(5)

    raise exc_


if __name__ == "__main__":
    client = docker.from_env()
    container = client.containers.run(
        "postgis/postgis",
        detach=True,
        name="geo",
        environment=ENV_VARS,
        ports={5432: 5432},
    )
    # give it a chance to start up

    try:
        setup_pg()
        create_tables()
    except Exception as e:
        print(traceback.format_exc())
        print(e)
        container.stop()
        # container.remove()
