from datetime import datetime
import Account

class Transaction:
    index: int
    date: datetime
    abstract: str
    debitAccount: Account
    creditAccount: Account
    amount: float
    def __init__(self,index:int,date:datetime,abstract:str,creditAccount:Account,debitAccount:Account,amount:float):
        self.index = index
        self.date = date
        self.abstract = abstract
        self.debitAccount = debitAccount
        self.creditAccount = creditAccount
        self.amount = amount