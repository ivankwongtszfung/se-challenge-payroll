from __future__ import annotations
from datetime import date


from app.models.period import Period


class EmploymentRecord:
    def __init__(self, id: int, work_date: date, pay_amount: float):
        self.id = id
        self.period = Period.from_date(work_date)
        self.pay_amount = pay_amount

    def as_dict(self):
        return {
            "employee_id": str(self.id),
            "pay_period": self.period.as_dict(),
            "amount_paid": "${:.2f}".format(self.pay_amount),
        }
