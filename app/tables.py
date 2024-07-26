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
from sqlalchemy.sql import or_, and_, not_
from sqlalchemy import (
    CheckConstraint,
    ForeignKey,
    String,
    TIMESTAMP,
    UUID,
)

# Internal libraries

Base = declarative_base()


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


class Feed(GISBase):
    __tablename__ = "feed"
    __table_args__ = {"schema": "gps"}
    name = mapped_column(String)


class FeedItem(GISBase):
    __tablename__ = "feed_item"
    __table_args__ = {"schema": "gps"}
    name = mapped_column(String)


class Trajectory(GISBase):
    __tablename__ = "trajectory"
    __table_args__ = (
        CheckConstraint(
            or_(
                mapped_column("feed_item_id").isnot(None),
                mapped_column("feed_id").isnot(None),
            ),
            name="check_feed_item_id_or_feed_id_not_null",
        ),
        CheckConstraint(
            not_(
                and_(
                    mapped_column("feed_item_id").isnot(None),
                    mapped_column("feed_id").isnot(None),
                )
            ),
            name="check_only_one_fk_not_null",
        ),
        {"schema": "gps"},
    )
    geom = mapped_column(Geometry("GEOMETRYZM"))
    feed_item_id = mapped_column(ForeignKey(FeedItem.id))
    feed_id = mapped_column(ForeignKey(Feed.id))
