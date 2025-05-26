from enum import Enum
from abc import ABC, abstractmethod
from Transaction import *
from pathlib import Path
import csv


class AccountType(Enum):
    DEFAULT = 0
    ASSET = 1
    LIABILITY = 2
    OWNERS_EQUITY = 3
    REVENUE = 4
    EXPENSE = 5
    PROFIT = 6

def accountTypeConvert(accType: str) -> AccountType:
    accType = accType.lower()
    if accType == "asset":
        return AccountType.ASSET
    elif accType == "liability":
        return AccountType.LIABILITY
    elif accType == "owners-equity":
        return AccountType.OWNERS_EQUITY
    elif accType == "revenue":
        return AccountType.REVENUE
    elif accType == "expense":
        return AccountType.EXPENSE
    elif accType == "profit":
        return AccountType.PROFIT
    else:
        return AccountType.DEFAULT

class Account(ABC):
    accountType: AccountType
    name: str
    balance: float
    filePath: Path
    header:list[str] = ["No.","date", "abstract", "debit", "credit", "balance"]

    @abstractmethod
    def handleCreditTransaction(self, transaction: Transaction):
        pass

    @abstractmethod
    def handleDebitTransaction(self,transaction: Transaction):
        pass

class CreditAccount(Account):
    def __init__(self, accountType: AccountType, name: str, initialBalance: float):
        self.accountType = accountType
        self.name = name
        self.balance = initialBalance
        self.filePath = Path(f"data/accounts/{name}.csv")
        with open(self.filePath, "w+", newline="") as fp:
            writer = csv.writer(fp)
            writer.writerow(self.header)
            writer.writerow([None, None, "期初余额", None, initialBalance, initialBalance])

    def handleCreditTransaction(self, transaction: Transaction):
        with open(self.filePath,"a+",newline="") as fp:
            writer = csv.writer(fp)
            self.balance += transaction.amount
            writer.writerow([transaction.index,transaction.date,transaction.abstract,transaction.amount,None,self.balance])

    def handleDebitTransaction(self,transaction: Transaction):
        with open(self.filePath,"a+",newline="") as fp:
            writer = csv.writer(fp)
            self.balance -= transaction.amount
            writer.writerow([transaction.index,transaction.date,transaction.abstract,None,transaction.amount,self.balance])

class DebitAccount(Account):
    def __init__(self, accountType: AccountType, name: str, initialBalance: float):
        self.accountType = accountType
        self.name = name
        self.balance = initialBalance
        self.filePath = Path(f"data/accounts/{name}.csv")
        with open(self.filePath, "w+", newline="") as fp:
            writer = csv.writer(fp)
            writer.writerow(self.header)
            writer.writerow([None, None, "期初余额", initialBalance, None, initialBalance])

    def handleCreditTransaction(self, transaction: Transaction):
        with open(self.filePath,"a+",newline="") as fp:
            writer = csv.writer(fp)
            self.balance -= transaction.amount
            writer.writerow([transaction.index,transaction.date,transaction.abstract,transaction.amount,None,self.balance])

    def handleDebitTransaction(self,transaction: Transaction):
        with open(self.filePath,"a+",newline="") as fp:
            writer = csv.writer(fp)
            self.balance += transaction.amount
            writer.writerow([transaction.index,transaction.date,transaction.abstract,None,transaction.amount,self.balance])