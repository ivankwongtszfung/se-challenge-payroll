from datetime import date

import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.models import Timesheet
from app.tests import Session


class TimesheetFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Timesheet
        sqlalchemy_session = Session

    id = factory.Faker("pyint")
    path = factory.Faker("file_path")
    date = factory.LazyFunction(date.today)
