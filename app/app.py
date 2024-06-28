#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By: K Agajanian

# Standard libraries
import json

# External libraries
from sanic import Sanic, response, HTTPResponse
# from sanic.response import json

from sqlalchemy import select, func, text
from sqlalchemy.orm import sessionmaker

# Internal libraries
from db_setup import engine_go_vroom
from db_setup import Trajectory


app = Sanic("gis-app")


@app.route("/")
def get(request):
    engine = engine_go_vroom()
    Session = sessionmaker(bind=engine)
    session = Session()

    # TODO: Currently hard-coded to get a single trajectory
    q = select(Trajectory, func.ST_AsText(Trajectory.geom).label("geom")).where(
        Trajectory.id == 2
    )  # select
    q = text(
        "SELECT ST_AsText(geom), feed_item_id FROM gps.trajectory WHERE id = 2"
    )  # text

    with session as s:
        trajs = s.execute(q).scalars().one_or_none()

    # return response.json(trajs.to_dict())  # for select stmt
    return response.json(trajs)  # for text stmt


@app.post("/")
def post(request):
    engine = engine_go_vroom()
    Session = sessionmaker(bind=engine)
    session = Session()

    gps_data = parse_data(request.body)

    try:
        with session as s:
            s.add_all(gps_data)
            s.commit()

        return HTTPResponse(status=202)

    except Exception as e:
        print(e)
        return HTTPResponse(status=400)


def parse_data(data):
    data = json.loads(data)
    feed_item_id = data["feed_item_id"]
    del data["feed_item_id"]

    data = data["gps_data"]

    # Create rows from sample data
    gps_data = [
        Trajectory(
            geom=f"SRID=4326;LINESTRINGZM({data})",
            feed_item_id=feed_item_id,
        )
    ]
    return gps_data


if __name__ == "__main__":
    app.run()
