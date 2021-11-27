from calendar import monthrange
from dataclasses import dataclass, field
from datetime import date
from enum import Enum

PAYPERIOD_CUTOFF = 15


class PayPeriod(Enum):
    FIRST = 1
    SECOND = PAYPERIOD_CUTOFF + 1

    @classmethod
    def from_date(cls, _date):
        return cls.FIRST if _date.day <= PAYPERIOD_CUTOFF else cls.SECOND


@dataclass
class Period:
    date: date
    pay_period: PayPeriod

    @classmethod
    def from_date(cls, _date: date):
        return cls(
            date=date(_date.year, _date.month, 1),
            pay_period=PayPeriod.from_date(_date),
        )

    def get_date_range(self):
        year, month = self.date.year, self.date.month
        start = date(year, month, self.pay_period.value)
        if self.pay_period == PayPeriod.FIRST:
            return start, date(year, month, PAYPERIOD_CUTOFF)
        elif self.pay_period == PayPeriod.SECOND:
            _, end = monthrange(year, month)
            return start, date(year, month, end)

    def as_dict(self):
        start, end = self.get_date_range()
        return {
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
        }
