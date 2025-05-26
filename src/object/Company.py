from Account import *
from Transaction import *
from src.userInterface.CommandLine import *
from src.utils.Analyzer import *
from src.utils.Reporter import *


class Company:
    name: str
    accounts: dict[str:Account]
    transactions: list[Transaction]
    analyzer: Analyzer
    reporter: Reporter
    report: Report

    def __init__(self, name: str):
        self.name = name
        self.accounts = {}
        self.transactions = []
        analyzer = Analyzer(self)
        reporter = Reporter(self)
        report = Report()

    def initAccounts(self):
        #todo: initialize a few accounts, must check if the amount is balanced
        return

    def createAccount(self, accountType: AccountType, name: str, initialBalance: float):
        if accountType == AccountType.ASSET or accountType == AccountType.PROFIT or accountType == AccountType.EXPENSE:
            self.accounts[name] = CreditAccount(accountType, name, initialBalance)
        elif accountType == AccountType.LIABILITY or accountType == AccountType.OWNERS_EQUITY or accountType == AccountType.REVENUE:
            self.accounts[name] = DebitAccount(accountType, name, initialBalance)
        else:
            print("Opps, invalid account type. Try again.")

    def addTransaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def checkTransactionAccounts(self,transaction:Transaction)->bool:
        if transaction.creditAccountName not in self.accounts:
            ans = input(f"{transaction.creditAccountName} does not exist. Do you want to create it?(Y/N)")
            if ans == "Y":
                accountType: str = input("Type of the account: ")
                command:Command = Command("create-account",{"accountType":accountType,"name":transaction.creditAccountName})
                self.executeCommand(command)
            else:
                return False
        if transaction.debitAccountName not in self.accounts:
            ans = input(f"{transaction.debitAccountName} does not exist. Do you want to create it?(Y/N)")
            if ans == "Y":
                accountType: str = input("Type of the account: ")
                command:Command = Command("create-account",{"accountType":accountType,"name":transaction.creditAccountName})
                self.executeCommand(command)
            else:
                return False
        return True

    def checkNullData(self,transaction)->bool:
        return ((not transaction.date is None) and (not transaction.creditAccountName is None)
            and (not transaction.debitAccountName is None) and (not transaction.amount is None))

    def handleTransaction(self, transaction: Transaction):
        if  self.checkNullData(transaction) and self.checkTransactionAccounts(transaction):
            creditSide:Account = self.accounts[transaction.creditAccountName]
            debitSide:Account = self.accounts[transaction.debitAccountName]
            creditSide.handleCreditTransaction(transaction)
            debitSide.handleDebitTransaction(transaction)
            self.addTransaction(transaction)
        else:
            print("Invalid transaction! Try again!")

    def formReport(self):
        self.reporter.formReport()

    def displayReport(self):
        self.reporter.displayReport()

    def analyzeData(self):
        self.analyzer.analyze()

    def executeCommand(self,command:Command):
        #todo: execute a command
        return