from sqlalchemy import TIMESTAMP, Column, Integer, Numeric, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CalcResult(Base):
    __tablename__ = "calc_results"

    id = Column(Integer, primary_key=True, index=True)
    total_cost_rub = Column(Numeric(10, 2), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now(), nullable=False)

