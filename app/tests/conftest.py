from pytest import fixture
import sqlalchemy

from app.models.base import Base
from app.tests import Session

# Base.metadata.create_all(bind=engine)


@fixture
def test_db_session():
    try:
        engine = sqlalchemy.create_engine("sqlite://")
        Session.configure(bind=engine)
        Base.metadata.create_all(bind=engine)
        yield Session()
    finally:
        Session.rollback()
        Session.remove()
