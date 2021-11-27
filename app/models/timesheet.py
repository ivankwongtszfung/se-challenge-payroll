from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String

from app.models.base import Base


class Timesheet(Base):
    __tablename__ = "timesheets"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, unique=True, nullable=False)
    date = Column(DateTime, default=datetime.now)
