import factory
from factory.alchemy import SQLAlchemyModelFactory

from app.models import JobGroup
from app.tests import Session


class JobGroupFactory(SQLAlchemyModelFactory):
    class Meta:
        model = JobGroup
        sqlalchemy_session = Session

    name = factory.Faker("pystr")
    hourly_pay = factory.Faker("pyint")
