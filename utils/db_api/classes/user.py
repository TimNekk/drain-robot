from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    id: int
    paid: int
    used: int
    date: datetime

    def add_paid(self):
        pass