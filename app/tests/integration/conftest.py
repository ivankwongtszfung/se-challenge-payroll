from fastapi.testclient import TestClient
from pytest import fixture

from app.main import app
from app.models.base import Base, get_db
from app.tests import Session, engine, override_get_db
from app.tests.factories.job_group import JobGroupFactory


@fixture
def test_client():
    client = TestClient(app)
    app.dependency_overrides[get_db] = override_get_db
    Base.metadata.create_all(bind=engine)
    yield client
    Base.metadata.drop_all(bind=engine)


@fixture
def test_job_group(test_client):
    JobGroupFactory(name="A", hourly_pay=20)
    JobGroupFactory(name="B", hourly_pay=30)
    Session.commit()
