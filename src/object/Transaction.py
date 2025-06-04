from datetime import datetime

class Transaction:
    index: int
    date: datetime
    abstract: str
    debitAccountName: str
    creditAccountName: str
    amount: float

    def __init__(self,index:int,date:datetime,abstract:str,debitAccountName:str,creditAccountName:str,amount:float):
        self.index = index
        self.date = date
        self.abstract = abstract
        self.debitAccountName = debitAccountName
        self.creditAccountName = creditAccountName
        self.amount = amount

    def getTransactionInfo(self)->dict:
        return {
            "index": self.index,
            "date": self.date,
            "abstract": self.abstract,
            "debitAccountName": self.debitAccountName,
            "creditAccountName": self.creditAccountName,
            "amount": self.amount
        }
