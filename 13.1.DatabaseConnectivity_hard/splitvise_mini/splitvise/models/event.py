# import datetime

from sqlalchemy import Integer, Column, DateTime, Boolean, String
# from sqlalchemy.orm import relationship

from .base import Base


class Event(Base):  # type: ignore
    __tablename__ = 'events'

    # TODO: fix me
    event_id = Column(Integer, primary_key=True)
    trip_id = Column(Integer)
    title = Column(String)
    happened_datetime = Column(DateTime)
    settled_up = Column(Boolean)
