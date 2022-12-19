from sqlalchemy import Column, Integer,  Numeric
# from sqlalchemy.orm import relationship

from .base import Base


class Expense(Base):  # type: ignore
    __tablename__ = 'expenses'

    # TODO: fix me
    expense_id = Column(Integer, primary_key=True)
    event_id = Column(Integer)
    payer_id = Column(Integer)
    value = Column(Numeric)
