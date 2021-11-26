import csv
from datetime import datetime

from pytest import fixture

from app.services.timesheet import WorkRecord


@fixture
def date(faker):
    return faker.date()


@fixture
def working_hour(faker):
    return "{:.1f}".format(faker.pyfloat() % 24)


@fixture
def employee_id(faker):
    return faker.pyint()


@fixture
def job_group(faker):
    return "A"


@fixture
def work_record(date, employee_id, working_hour, job_group):
    return WorkRecord(
        date=date,
        employee_id=employee_id,
        job_group=job_group,
        working_hour=working_hour,
    )


@fixture
def timesheet_data(date, employee_id, working_hour, job_group):
    return {
        "date": date,
        "hours worked": working_hour,
        "employee id": employee_id,
        "job group": job_group,
    }


@fixture
def timesheet_header(timesheet_data):
    return list(timesheet_data.keys())
