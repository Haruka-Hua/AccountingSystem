from datetime import datetime

class Transaction:
    index: int
    date: datetime
    abstract: str
    debitAccountName: str
    creditAccountName: str
    amount: float

    def __init__(self,index:int,date:datetime,abstract:str,creditAccountName:str,debitAccountName:str,amount:float):
        self.index = index
        self.date = date
        self.abstract = abstract
        self.creditAccountName = creditAccountName
        self.debitAccountName = debitAccountName
        self.amount = amount