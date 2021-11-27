from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base


class WorkRecord(Base):
    __tablename__ = "work_records"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, nullable=False)
    job_group_name = Column(String, ForeignKey("job_groups.name"), nullable=False)
    work_hour = Column(Float, nullable=False)
    date = Column(Date, nullable=False)
    report_id = Column(Integer, ForeignKey("timesheets.id"))
    job_group = relationship("JobGroup")
    report = relationship("Timesheet")
