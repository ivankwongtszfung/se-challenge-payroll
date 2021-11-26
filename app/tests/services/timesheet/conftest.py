import csv
from datetime import date

from pytest import fixture

from app.services.timesheet import WorkRecord


@fixture
def work_date(faker):
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
def work_record(work_date, employee_id, working_hour, job_group):
    return WorkRecord(
        date=date.fromisoformat(work_date),
        employee_id=employee_id,
        job_group=job_group,
        working_hour=float(working_hour),
    )


@fixture
def timesheet_data(work_date, employee_id, working_hour, job_group):
    return {
        "date": work_date,
        "hours worked": working_hour,
        "employee id": employee_id,
        "job group": job_group,
    }


@fixture
def timesheet_header(timesheet_data):
    return list(timesheet_data.keys())
