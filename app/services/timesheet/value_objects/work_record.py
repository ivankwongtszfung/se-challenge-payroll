from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from app.models import Period


DATEFORMAT = "%d/%m/%Y"


@dataclass
class WorkRecord:
    employee_id: int
    job_group: str
    working_hour: float
    date: date

    @classmethod
    def from_timesheet(cls, timesheet: dict) -> WorkRecord:
        return cls(
            employee_id=int(timesheet["employee id"]),
            working_hour=float(timesheet["hours worked"]),
            date=datetime.strptime(timesheet["date"], DATEFORMAT).date(),
            job_group=timesheet["job group"],
        )

    def period(self) -> Period:
        return Period(self.date.day > 15)

    def as_dict(self):
        return {
            "employee_id": self.employee_id,
            "job_group_name": self.job_group,
            "work_hour": self.working_hour,
            "date": self.date,
        }
