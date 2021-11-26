import csv
from io import StringIO

from pytest import fixture, raises

from app.services.timesheet import TimesheetParser


@fixture
def csvfile():
    return StringIO()


@fixture
def csv_writer(timesheet_header, csvfile):
    return csv.DictWriter(csvfile, fieldnames=timesheet_header)


@fixture
def time_report_header_only(csvfile, csv_writer):
    csv_writer.writeheader()
    csvfile.seek(0)
    return csvfile


@fixture
def time_report_one_row(csvfile, csv_writer, timesheet_data):
    csv_writer.writeheader()
    csv_writer.writerow(timesheet_data)
    csvfile.seek(0)
    return csvfile


@fixture
def no_of_row(faker):
    return faker.pyint(min_value=5, max_value=10)


@fixture
def time_report(csvfile, csv_writer, timesheet_data, no_of_row):
    csv_writer.writeheader()
    for _ in range(no_of_row):
        csv_writer.writerow(timesheet_data)
    csvfile.seek(0)
    return csvfile


# no rows
def test_parse_one_stop_iterate_when_no_data(time_report_header_only):
    with raises(StopIteration):
        next(TimesheetParser().parse_one(time_report_header_only))


def test_parse_all_return_empty_list_when_no_data(time_report_header_only):
    assert TimesheetParser().parse_all(time_report_header_only) == []


# one row
def test_parse_one(time_report_one_row, work_record):
    assert next(TimesheetParser().parse_one(time_report_one_row)) == work_record


def test_parse_all(time_report_one_row, work_record):
    assert TimesheetParser().parse_all(time_report_one_row) == [work_record]


# x rows
def test_parse_one_read_all_rows(time_report, work_record, no_of_row):
    count = 0
    for loaded_record in TimesheetParser().parse_one(time_report):
        assert loaded_record == work_record
        count += 1
    assert count == no_of_row, "Parser doesn't run all the rows"


def test_parse_all_read_all_rows(time_report, no_of_row):
    assert (
        len(TimesheetParser().parse_all(time_report)) == no_of_row
    ), "Parser doesn't run all the rows"
