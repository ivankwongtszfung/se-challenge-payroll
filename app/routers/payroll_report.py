from datetime import date
from typing import Dict, List

from fastapi import APIRouter
from fastapi_camelcase import CamelModel

from app.models.base import SessionLocal
from app.services.employment_report import EmploymentReport

router = APIRouter(prefix="/payroll_report", tags=["payroll_report"])


class PayPeriod(CamelModel):
    start_date: date
    end_date: date


class EmployeeReports(CamelModel):
    employee_id: str
    pay_period: PayPeriod
    amount_paid: str


class PayrollReport(CamelModel):
    employee_reports: List[EmployeeReports]


@router.get("/", response_model=Dict[str, PayrollReport])
async def get_employee_reports():
    with SessionLocal() as session:
        return {
            "payroll_report": {
                "employee_reports": EmploymentReport(db=session).create()
            }
        }
