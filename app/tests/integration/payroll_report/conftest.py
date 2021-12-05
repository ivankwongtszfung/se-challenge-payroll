from fastapi.testclient import TestClient
from pytest import fixture

from app.tests import Session
from app.tests.factories.job_group import JobGroupFactory


@fixture
def test_job_group(test_client):
    JobGroupFactory(name="A", hourly_pay=20)
    JobGroupFactory(name="B", hourly_pay=30)
    Session.commit()
