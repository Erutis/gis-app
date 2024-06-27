#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By: K Agajanian
# Created: 2/21/24
# as of 3/6/24 this fucking works!!

# Standard libraries
from datetime import datetime, timezone

import enum


# External libraries

# Internal libraries


import time
import traceback

from geoalchemy2 import Geometry
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    schema,
    text,
    TIMESTAMP,
    UUID,
)

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm.state import InstanceState


ENV_VARS = {
    "POSTGRES_HOST": "db",
    "MYDB__DATABASE": "nyc",
    "POSTGRES_USER": "nyc",
    "MYDB__PORT": 5432,
    "MYDB__DRIVERNAME": "postgresql",
    "POSTGRES_PASSWORD": "gis",
    "platform": "linux/amd64",
}

POSTGRES_HOST = ENV_VARS["POSTGRES_HOST"]
DB = ENV_VARS["MYDB__DATABASE"]
DRIVERNAME = ENV_VARS["MYDB__DRIVERNAME"]
USER = ENV_VARS["POSTGRES_USER"]
PW = ENV_VARS["POSTGRES_PASSWORD"]
PORT = ENV_VARS["MYDB__PORT"]


Base = declarative_base()


class Trajectory(Base):
    __tablename__ = "trajectory"
    # __table_args__ = {"schema": "gps"}
    id = Column(Integer, primary_key=True)
    create_time = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_time = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    geom = Column(Geometry("LINESTRINGZM"))
    feed_item_id = Column(UUID)

    def to_dict(self):
        d = {}

        for field, value in self.__dict__.items():
            if any(
                (
                    isinstance(value, InstanceState),
                    isinstance(value, list),
                )
            ):
                continue
            if isinstance(value, (int, float, bool, str, type(None))):
                d[field] = value
            elif isinstance(value, enum.Enum):
                d[field] = value.name
            else:
                d[field] = str(value)

        return d


def setup_pg():
    """Create GIS engine, connect, and create tables."""
    # Start sqlalchemy engine & wait for connection
    engine = engine_go_vroom()
    pg_check(engine=engine)

    # # Create Postgis extension, Trajectory table, and commit
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


def engine_go_vroom():
    url = f"{DRIVERNAME}://{USER}:{PW}@{POSTGRES_HOST}:{PORT}/{DB}"
    engine = create_engine(url, echo=True)

    return engine


if __name__ == "__main__":
    try:
        setup_pg()
        print("DB set up!")
    except Exception as e:
        print(traceback.format_exc())
        print(e)
