from dataclasses import dataclass
from datetime import datetime, timedelta
from uuid import uuid4

import pyqiwi

from data.config import Qiwi

wallet = pyqiwi.Wallet(token=Qiwi.token, number=Qiwi.wallet)


class NotEnoughMoney(Exception):
    pass


class NoPaymentFound(Exception):
    pass


@dataclass
class Payment:
    amount: int
    id: str = None

    def create(self):
        self.id = str(uuid4())

    def check_payment(self):
        transactions = wallet.history(
            start_date=datetime.now() - timedelta(days=2)
        ).get('transactions')

        for transaction in transactions:
            if transaction.comment:
                if str(self.id) in transaction.comment:
                    if float(transaction.total.amount) >= float(self.amount):
                        return True
                    else:
                        raise NotEnoughMoney
        else:
            raise NoPaymentFound

    @property
    def invoice(self):
        link = f"https://oplata.qiwi.com/create?publicKey={Qiwi.public_key}&" \
               f"amount={self.amount}&" \
               f"comment={self.id}&" \
               f"successUrl=t.me/nudes_robot&" \
               f"customFields[themeCode]={Qiwi.themeCode}"
        return link