from __future__ import annotations
from dataclasses import dataclass
from datetime import date


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
            date=date.fromisoformat(timesheet["date"]),
            job_group=timesheet["job group"],
        )
