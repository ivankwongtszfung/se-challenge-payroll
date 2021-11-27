from datetime import date

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.models import WorkRecord
from app.tests import Session
from app.tests.factories.job_group import JobGroupFactory
from app.tests.factories.timesheet import TimesheetFactory


class WorkRecordFactory(SQLAlchemyModelFactory):
    class Meta:
        model = WorkRecord
        sqlalchemy_session = Session

    employee_id = factory.Faker("pyint")
    work_hour = factory.Faker("pyfloat")
    date = factory.LazyFunction(date.today)
    job_group = factory.SubFactory(JobGroupFactory)
    report = factory.SubFactory(TimesheetFactory)
