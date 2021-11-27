from sqlalchemy import Column, Float, String

from app.models.base import Base


class JobGroup(Base):
    __tablename__ = "job_groups"

    name = Column(String, primary_key=True, index=True)
    hourly_pay = Column(Float, nullable=False)
