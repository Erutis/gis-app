#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# By: K Agajanian

# Standard libraries
from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

import enum

# External libraries
from geoalchemy2 import Geometry
from sqlalchemy.orm import declarative_base, mapped_column
from sqlalchemy.orm.state import InstanceState
from sqlalchemy import (
    ForeignKey,
    String,
    TIMESTAMP,
    UUID,
)
from sqlalchemy import MetaData

# Internal libraries

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class GISBase(Base):
    __abstract__ = True
    id = mapped_column(
        UUID, primary_key=True, nullable=False, index=True, default=lambda: str(uuid4())
    )
    create_time = mapped_column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_time = mapped_column(TIMESTAMP, default=datetime.now(timezone.utc))

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


class FeedItem(GISBase):
    __tablename__ = "feed_item"
    __table_args__ = {"schema": "gps"}
    name = mapped_column(String)


class Trajectory(GISBase):
    __tablename__ = "trajectory"
    __table_args__ = {"schema": "gps"}
    geom = mapped_column(Geometry("GEOMETRYZM", spatial_index=False))
    feed_item_id = mapped_column(ForeignKey(FeedItem.id))
