from pathlib import Path

from pytest import fixture

from app.main import app


@fixture
def time_report():
    with open(
        Path(__file__).parent.joinpath("static_files", "time_report_all.csv").resolve()
    ) as f:
        yield f, "time-report-1.csv"


@fixture
def time_report_part1():
    return (
        open(
            Path(__file__)
            .parent.joinpath("static_files", "time_report_part1.csv")
            .resolve()
        ),
        "time-report-2.csv",
    )


@fixture
def time_report_part2():
    return (
        open(
            Path(__file__)
            .parent.joinpath("static_files", "time_report_part2.csv")
            .resolve()
        ),
        "time-report-3.csv",
    )


@fixture
def time_resport_result(test_job_group):
    return {
        "payrollReport": {
            "employeeReports": [
                {
                    "employeeId": "1",
                    "payPeriod": {"startDate": "2023-11-01", "endDate": "2023-11-15"},
                    "amountPaid": "$150.00",
                },
                {
                    "employeeId": "1",
                    "payPeriod": {"startDate": "2023-11-16", "endDate": "2023-11-30"},
                    "amountPaid": "$220.00",
                },
                {
                    "employeeId": "1",
                    "payPeriod": {"startDate": "2023-12-01", "endDate": "2023-12-15"},
                    "amountPaid": "$150.00",
                },
                {
                    "employeeId": "1",
                    "payPeriod": {"startDate": "2023-12-16", "endDate": "2023-12-31"},
                    "amountPaid": "$220.00",
                },
                {
                    "employeeId": "2",
                    "payPeriod": {"startDate": "2023-11-01", "endDate": "2023-11-15"},
                    "amountPaid": "$930.00",
                },
                {
                    "employeeId": "2",
                    "payPeriod": {"startDate": "2023-12-01", "endDate": "2023-12-15"},
                    "amountPaid": "$930.00",
                },
                {
                    "employeeId": "3",
                    "payPeriod": {"startDate": "2023-11-01", "endDate": "2023-11-15"},
                    "amountPaid": "$590.00",
                },
                {
                    "employeeId": "3",
                    "payPeriod": {"startDate": "2023-12-01", "endDate": "2023-12-15"},
                    "amountPaid": "$470.00",
                },
                {
                    "employeeId": "4",
                    "payPeriod": {"startDate": "2023-02-16", "endDate": "2023-02-28"},
                    "amountPaid": "$150.00",
                },
                {
                    "employeeId": "4",
                    "payPeriod": {"startDate": "2023-11-01", "endDate": "2023-11-15"},
                    "amountPaid": "$150.00",
                },
                {
                    "employeeId": "4",
                    "payPeriod": {"startDate": "2023-11-16", "endDate": "2023-11-30"},
                    "amountPaid": "$450.00",
                },
                {
                    "employeeId": "4",
                    "payPeriod": {"startDate": "2023-12-01", "endDate": "2023-12-15"},
                    "amountPaid": "$150.00",
                },
                {
                    "employeeId": "4",
                    "payPeriod": {"startDate": "2023-12-16", "endDate": "2023-12-31"},
                    "amountPaid": "$450.00",
                },
            ]
        }
    }


def test_payroll_report_created_correctly(
    test_client, time_report, time_resport_result
):
    report, filename = time_report
    response = test_client.post(
        "/timesheet/file/",
        files={"file": (filename, report, "text/csv")},
    )
    assert response.ok, f"Cannot post file {response.text}"
    response = test_client.get("/payroll_report/")
    assert response.json() == time_resport_result


def test_payroll_report_created_correctly_even_split_in_two_files(
    test_client, time_report_part1, time_report_part2, time_resport_result
):

    time_reports = [time_report_part1, time_report_part2]
    for report, filename in time_reports:
        response = test_client.post(
            "/timesheet/file/",
            files={"file": (filename, report, "text/csv")},
        )
    assert response.ok, f"Cannot post file {response.text}"
    response = test_client.get("/payroll_report/")
    assert response.json() == time_resport_result


def test_payroll_report_conflicts_when_upload_report_with_same_name(
    test_client, time_report, time_resport_result
):

    time_reports = [time_report, time_report]
    for report, filename in time_reports:
        response = test_client.post(
            "/timesheet/file/",
            files={"file": (filename, report, "text/csv")},
        )
    assert response.status_code == 409
