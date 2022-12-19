from sqlalchemy import Integer, Column, Numeric
# from sqlalchemy.orm import relationship

from .base import Base


class Summary(Base):  # type: ignore
    __tablename__ = 'summaries'

    # TODO: fix me
    summary_id = Column(Integer, primary_key=True)
    trip_id = Column(Integer)
    user_from_id = Column(Integer)
    user_to_id = Column(Integer)
    value = Column(Numeric)
