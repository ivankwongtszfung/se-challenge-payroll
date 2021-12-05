from datetime import date
from typing import Dict, List

from fastapi import APIRouter, Depends
from fastapi_camelcase import CamelModel
from sqlalchemy.orm import Session

from app.models.base import get_db
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
async def get_employee_reports(session: Session = Depends(get_db)):
    return {
        "payroll_report": {"employee_reports": EmploymentReport(db=session).create()}
    }
