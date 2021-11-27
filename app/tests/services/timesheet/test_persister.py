from pytest import fixture, raises

from app.models import Timesheet, WorkRecord
from app.services.timesheet.persister import TimesheetDBPersister
from app.tests.factories.timesheet import TimesheetFactory


@fixture
def data_persister(test_db_session):
    return TimesheetDBPersister(db=test_db_session)


@fixture
def timesheet(test_db_session):
    return TimesheetFactory()


def test_db_persister_insert_row_success(
    test_db_session, data_persister, timesheet, work_record
):
    data_persister.save_record(timesheet, [work_record])
    assert test_db_session.query(WorkRecord).count()


def test_db_persister_cannot_insert_report_success(
    test_db_session, data_persister, faker
):
    data_persister.save_report(report_id=faker.pyint(), path="")
    assert test_db_session.query(Timesheet).count()


def test_db_persister_cannot_insert_report_again(
    test_db_session, data_persister, faker, timesheet
):
    with raises(Exception):
        data_persister.save_report(report_id=timesheet.id, path="")
