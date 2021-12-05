from pytest import fixture, raises

from app.models import Timesheet, WorkRecord
from app.services.timesheet.persister import TimesheetDBPersister
from app.tests.factories.timesheet import TimesheetFactory


@fixture
def data_persister(test_db_session):
    return TimesheetDBPersister(db=test_db_session)


@fixture
def timesheet(test_db_session):
    sheet = TimesheetFactory()
    test_db_session.commit()
    return sheet


def test_db_persister_check_exists_return_true(
    test_db_session, data_persister, timesheet, work_record
):
    assert data_persister.check_report_exists(timesheet.id)


def test_db_persister_check_exists_return_false_when_id_not_the_same(
    test_db_session, data_persister, timesheet, work_record
):
    assert data_persister.check_report_exists(timesheet.id + 1) is None


def test_db_persister_insert_row_success(
    test_db_session, data_persister, timesheet, work_record
):
    data_persister.save_record(timesheet, [work_record])
    test_db_session.commit()
    assert test_db_session.query(WorkRecord).count()


def test_db_persister_cannot_insert_report_success(
    test_db_session, data_persister, faker
):
    data_persister.save_report(report_id=faker.pyint(), path="")
    test_db_session.commit()
    assert test_db_session.query(Timesheet).count()
