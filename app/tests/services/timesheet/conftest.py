import csv
from datetime import date

from pytest import fixture

from app.services.timesheet import WorkRecord


@fixture
def fake_date(faker):
    return faker.date_between()


@fixture
def work_date(fake_date):
    return fake_date.strftime("%d/%m/%Y")


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
def work_record(fake_date, employee_id, working_hour, job_group):
    return WorkRecord(
        date=fake_date,
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
