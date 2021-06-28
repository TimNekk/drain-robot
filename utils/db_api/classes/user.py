from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    newid: int
    id: int
    paid: int
    used: int
    date: datetime

    def add_paid(self):
        pass