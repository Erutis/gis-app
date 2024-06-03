#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By: K Agajanian

# Standard libraries

# External libraries
from sanic import Sanic
from sanic.response import json

from sqlalchemy import select
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

    q = select(Trajectory)
    with session as s:
        trajs = s.execute(q).scalars().all()
        print(trajs)

    return trajs


if __name__ == "__main__":
    app.run()
