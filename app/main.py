from fastapi import FastAPI

from app.routers import payroll_report, timesheet


app = FastAPI()


app.include_router(payroll_report.router)
app.include_router(timesheet.router)
