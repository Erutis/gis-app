#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By: K Agajanian

# Standard libraries
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

import enum
import os
import time
import traceback


# External libraries
from geoalchemy2 import Geometry
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.orm.state import InstanceState
from sqlalchemy import (
    CheckConstraint,
    create_engine,
    Column,
    ForeignKey,
    schema,
    String,
    text,
    TIMESTAMP,
    UUID,
)

# Internal libraries

Base = declarative_base()


class GISBase(Base):
    __abstract__ = True
    id = Column(
        UUID, primary_key=True, nullable=False, index=True, default=lambda: str(uuid4())
    )
    create_time = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_time = Column(TIMESTAMP, default=datetime.now(timezone.utc))

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


class Project(GISBase):
    __tablename__ = "project"
    __table_args__ = {"schema": "gps"}
    name = Column(String)


class FeedItem(GISBase):
    __tablename__ = "feed_item"
    __table_args__ = {"schema": "gps"}
    name = Column(String)


class Trajectory(GISBase):
    __tablename__ = "trajectory"
    __table_args__ = (
        CheckConstraint(
            "feed_item_id IS NOT NULL OR project_id IS NOT NULL",
            name="check_feed_item_id_or_project_id_not_null",
        ),
        CheckConstraint(
            "NOT (feed_item_id IS NOT NULL AND project_id IS NOT NULL)",
            name="check_only_one_fk_not_null",
        ),
        {"schema": "gps"},
    )
    geom = Column(Geometry("GEOMETRYZM"))
    feed_item_id = Column(ForeignKey(FeedItem.id))
    project_id = Column(ForeignKey(Project.id))
