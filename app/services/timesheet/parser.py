from csv import DictReader
from typing import Iterator, List

from app.services.timesheet.value_objects.work_record import WorkRecord


class TimesheetParser:
    def parse_all(self, time_report) -> List[WorkRecord]:
        reader = DictReader(time_report)
        return [WorkRecord.from_timesheet(row) for row in reader]

    def parse_one(self, time_report) -> Iterator[WorkRecord]:
        reader = DictReader(time_report)
        for row in reader:
            yield WorkRecord.from_timesheet(row)
