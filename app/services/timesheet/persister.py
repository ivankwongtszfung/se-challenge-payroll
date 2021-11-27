from typing import List
from sqlalchemy.orm import Session

from app.models import WorkRecord
from app.models.timesheet import Timesheet
from app.services import timesheet


class TimesheetDBPersister:
    def __init__(self, db: Session):
        self.db = db

    def save_report(self, report_id: int, path: str) -> Timesheet:
        report = Timesheet(id=report_id, path=path)
        self.db.add(report)
        self.db.commit()
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
        self.db.commit()
        return db_work_records
