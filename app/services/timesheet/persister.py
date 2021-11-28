from typing import List

from sqlalchemy import literal
from sqlalchemy.orm import Session

from app.models import Timesheet, WorkRecord
from app.services import timesheet


class TimesheetDBPersister:
    def __init__(self, db: Session):
        self.db = db

    def check_report_exists(self, report_id):
        q = self.db.query(Timesheet).filter(Timesheet.id == report_id)
        return self.db.query(literal(True)).filter(q.exists()).scalar()

    def save_report(self, report_id: int, path: str) -> Timesheet:
        report = Timesheet(id=report_id, path=path)
        self.db.add(report)
        return report

    def save_record(
        self, report: Timesheet, work_records: List[timesheet.WorkRecord]
    ) -> List[WorkRecord]:
        db_work_records = []
        for work_record in work_records:
            work_record = WorkRecord(**work_record.as_dict())
            work_record.report = report
            self.db.add(work_record)
            db_work_records.append(work_record)
        return db_work_records
