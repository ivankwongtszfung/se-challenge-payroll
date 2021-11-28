from datetime import date
from typing import Dict, List
from codecs import iterdecode
import re

from fastapi import APIRouter, File, UploadFile
from fastapi_camelcase import CamelModel

from app.models.base import SessionLocal
from app.services.employment_report import EmploymentReport
from app.services.timesheet import TimesheetParser
from app.services.timesheet.persister import TimesheetDBPersister

router = APIRouter(prefix="/timesheet", tags=["timesheet"])


FILENAME_FORMAT = "time-report-(\d+).csv"


@router.post("/file/", status_code=204)
async def create_upload_file(file: UploadFile = File(...)):
    report_id = re.match(FILENAME_FORMAT, file.filename).group(1)
    work_records = TimesheetParser().parse_all(iterdecode(file.file, "utf-8"))
    with SessionLocal() as session:
        db_persister = TimesheetDBPersister(db=session)
        report = db_persister.save_report(report_id, file.filename)
        db_persister.save_record(report, work_records)
    return
