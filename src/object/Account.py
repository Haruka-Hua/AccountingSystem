import enum
from abc import ABC, abstractmethod
from Transaction import *
from pathlib import Path
import csv

class AccountType(enum):
    DEFAULT = 0
    ASSET = 1
    LIABILITY = 2
    OWNERS_EQUITY = 3
    REVENUE = 4
    EXPENSE = 5
    PROFIT = 6

class Account(ABC):
    accountType: AccountType
    name: str
    balance: float
    filePath: Path

    @abstractmethod
    def handleTransaction(self,transaction:Transaction):
        pass

class CreditAccount(Account):
    def __init__(self, accountType:AccountType, name:str, initialBalance:float):
        self.accountType = accountType
        self.name = name
        self.balance = initialBalance
        self.filePath = Path(f"data/accounts/{name}.csv")
        with open(self.filePath,"w",newline="") as fp:
            writer = csv.writer(fp)
            writer.writerow(["date","abstract","debit","credit","balance"])
            writer.writerow(["-","期初余额",None,initialBalance,initialBalance])

    def handleTransaction(self,transaction:Transaction):
        #todo
        return

class DebitAccount(Account):
    def __init__(self, accountType:AccountType, name:str, initialBalance:float):
        self.accountType = accountType
        self.name = name
        self.balance = initialBalance
        self.filePath = Path(f"data/accounts/{name}.csv")
        with open(self.filePath,"w",newline="") as fp:
            writer = csv.writer(fp)
            writer.writerow(["date","abstract","debit","credit","balance"])
            writer.writerow(["-","期初余额",initialBalance,None,initialBalance])

    def handleTransaction(self,transaction:Transaction):
        #todo
        return