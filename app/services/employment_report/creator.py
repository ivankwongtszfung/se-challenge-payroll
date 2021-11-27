from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import extract

from app.models import JobGroup, WorkRecord
from app.models.period import PAYPERIOD_CUTOFF
from app.services.employment_report import EmploymentRecord


class EmploymentReport:
    def __init__(self, db: Session):
        self.db = db
        self._report = {}

    def create(self):
        return [
            EmploymentRecord(*work_record).as_dict()
            for work_record in self._get_all_work_record()
        ]

    def _get_all_work_record(self):
        return (
            self.db.query(
                WorkRecord.employee_id,
                func.min(WorkRecord.date),
                func.sum(WorkRecord.work_hour) * JobGroup.hourly_pay,
            )
            .join(WorkRecord.job_group)
            .group_by(
                WorkRecord.employee_id,
                WorkRecord.job_group_name,
                extract("month", WorkRecord.date),
                extract("year", WorkRecord.date),
                extract("day", WorkRecord.date) <= PAYPERIOD_CUTOFF,
            )
            .order_by(WorkRecord.employee_id, WorkRecord.date)
            .all()
        )
