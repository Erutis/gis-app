#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By: K Agajanian

# Standard libraries
from functools import partial

# External libraries
from sanic import Sanic, response
from sanic.response import json

from sqlalchemy import select, func
from sqlalchemy.orm import sessionmaker

# Internal libraries
from db_setup import engine_go_vroom
from db_setup import Trajectory


app = Sanic("vrgis-app")


@app.route("/")
def get(request):
    engine = engine_go_vroom()
    Session = sessionmaker(bind=engine)
    session = Session()

    q = select(Trajectory, func.ST_AsText(Trajectory.geom).label("geom")).where(
        Trajectory.id == 2
    )

    with session as s:
        trajs = s.execute(q).scalars().one_or_none()

    result = trajs.to_dict()
    print(trajs)
    print(result)
    return response.json(result)


if __name__ == "__main__":
    app.run()
