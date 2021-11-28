import csv
from datetime import datetime

from pytest import fixture

from app.services.timesheet import WorkRecord


def test_from_timesheet(timesheet_data, work_record):
    assert WorkRecord.from_timesheet(timesheet_data) == work_record
