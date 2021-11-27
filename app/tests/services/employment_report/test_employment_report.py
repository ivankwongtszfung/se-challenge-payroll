from pytest import fixture
from datetime import date
from app.services.employment_report import EmploymentReport

from app.models import WorkRecord
from app.tests.factories.job_group import JobGroupFactory
from app.tests.factories.work_record import WorkRecordFactory


@fixture
def job_group_a(test_db_session):
    return JobGroupFactory(name="A", hourly_pay=20)


@fixture
def job_group_b(test_db_session):
    return JobGroupFactory(name="B", hourly_pay=30)


@fixture
def timesheet_record_same_period_n_id(test_db_session, job_group_a):
    return [
        WorkRecordFactory(
            date=date(2023, 1, 4),
            employee_id=1,
            job_group=job_group_a,
            work_hour=10,
        ),
        WorkRecordFactory(
            date=date(2023, 1, 14),
            employee_id=1,
            job_group=job_group_a,
            work_hour=5,
        ),
    ]


@fixture
def timesheet_record_differnt_id(test_db_session, job_group_b, job_group_a):
    return [
        WorkRecordFactory(
            date=date(2023, 1, 20),
            employee_id=1,
            job_group=job_group_a,
            work_hour=4,
        ),
        WorkRecordFactory(
            date=date(2023, 1, 20),
            employee_id=2,
            job_group=job_group_b,
            work_hour=3,
        ),
    ]


@fixture
def timesheet_record_different_period(
    test_db_session, timesheet_record_same_period_n_id, job_group_a
):
    return [
        *timesheet_record_same_period_n_id,
        WorkRecordFactory(
            date=date(2023, 1, 20),
            employee_id=1,
            job_group=job_group_a,
            work_hour=4,
        ),
    ]


@fixture
def employment_report(test_db_session):
    return EmploymentReport(db=test_db_session)


def test_employment_report_data_grouped(
    employment_report, timesheet_record_same_period_n_id
):
    assert employment_report.create() == [
        {
            "employee_id": "1",
            "pay_period": {"start_date": "2023-01-01", "end_date": "2023-01-15"},
            "amount_paid": "$300.00",
        }
    ]


def test_employment_report_differnt_people_not_grouped(
    employment_report, timesheet_record_differnt_id
):
    assert employment_report.create() == [
        {
            "employee_id": "1",
            "pay_period": {"start_date": "2023-01-16", "end_date": "2023-01-31"},
            "amount_paid": "$80.00",
        },
        {
            "employee_id": "2",
            "pay_period": {"start_date": "2023-01-16", "end_date": "2023-01-31"},
            "amount_paid": "$90.00",
        },
    ]


def test_employment_report_differnt_period_dont_join(
    employment_report, timesheet_record_different_period
):
    assert employment_report.create() == [
        {
            "employee_id": "1",
            "pay_period": {"start_date": "2023-01-01", "end_date": "2023-01-15"},
            "amount_paid": "$300.00",
        },
        {
            "employee_id": "1",
            "pay_period": {"start_date": "2023-01-16", "end_date": "2023-01-31"},
            "amount_paid": "$80.00",
        },
    ]
