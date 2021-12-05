import re
from codecs import iterdecode
from http import HTTPStatus

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, Response
from sqlalchemy.orm import Session

from app.models.base import get_db
from app.services.timesheet import TimesheetParser
from app.services.timesheet.persister import TimesheetDBPersister

router = APIRouter(prefix="/timesheet", tags=["timesheet"])


FILENAME_FORMAT = "time-report-(\d+).csv"


@router.post("/file/", status_code=HTTPStatus.NO_CONTENT.value)
async def create_upload_file(
    file: UploadFile = File(...), session: Session = Depends(get_db)
):
    report_id = re.match(FILENAME_FORMAT, file.filename).group(1)
    work_records = TimesheetParser().parse_all(iterdecode(file.file, "utf-8"))
    db_persister = TimesheetDBPersister(db=session)
    if db_persister.check_report_exists(report_id):
        raise HTTPException(
            status_code=409, detail=f"Report Id {report_id} already exists"
        )
    report = db_persister.save_report(report_id, file.filename)
    db_persister.save_record(report, work_records)
    session.commit()
    return Response(status_code=HTTPStatus.NO_CONTENT.value)

