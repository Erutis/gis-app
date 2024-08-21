#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By: K Agajanian
# Created: 2/21/24

# Standard libraries
import os
import time
import traceback


# External libraries
from sqlalchemy import (
    create_engine,
    schema,
    text,
)

# Internal libraries


def setup_pg():
    """Create GIS engine, connect, and create tables."""
    # Start sqlalchemy engine & wait for connection
    engine = engine_go_vroom()
    pg_check(engine=engine)

    # # Create Postgis extension and new schema
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS postgis"))
        conn.execute(text("SELECT postgis_full_version();"))
        conn.execute(schema.CreateSchema("henlo"))
        conn.commit()

        print("Schema created!")

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
    USER = os.getenv("POSTGRES_USER", "nyc")
    PW = os.getenv("POSTGRES_PASSWORD", "gis")
    DB = os.getenv("POSTGRES_DB", "nyc")
    HOST = os.getenv("POSTGRES_HOST", "localhost")
    DRIVERNAME = os.getenv("POSTGRES_DRIVERNAME", "postgresql")
    PORT = os.getenv("PORT", "5432")
    url = f"{DRIVERNAME}://{USER}:{PW}@{HOST}:{PORT}/{DB}"
    engine = create_engine(url, echo=True)

    return engine


if __name__ == "__main__":
    try:
        setup_pg()
        print("DB set up!")
    except Exception as e:
        print(traceback.format_exc())
        print(e)
