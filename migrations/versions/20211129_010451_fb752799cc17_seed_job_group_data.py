"""seed job group data

Revision ID: fb752799cc17
Revises: f17016370005
Create Date: 2021-11-29 01:04:51.591090

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm.session import Session

from app.models import JobGroup


# revision identifiers, used by Alembic.
revision = "fb752799cc17"
down_revision = "f17016370005"
branch_labels = None
depends_on = None


def upgrade():
    session = Session(bind=op.get_bind())
    session.add_all(
        [JobGroup(name="A", hourly_pay=20), JobGroup(name="B", hourly_pay=30)]
    )
    session.commit()


def downgrade():
    session = Session(bind=op.get_bind())
    session.delete(JobGroup).filter(JobGroup.name.in_(["A", "B"])).delete()
