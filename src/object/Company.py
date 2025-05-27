from pandas.core.interchange.dataframe_protocol import DataFrame

from Account import *
from Transaction import *
from src.userInterface.CommandLine import *
from src.utils.Analyzer import *
from src.utils.Reporter import *
import pandas
import os

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

    def initAccounts(self,accountInfo: pandas.DataFrame):
        for index, row in accountInfo.iterrows():
            accountType: AccountType = accountTypeConvert(row["accountType"])
            name: str = row["name"]
            initialBalance: float = float(row["initialBalance"])
            self.createAccount(accountType, name, initialBalance)
        #check balance
        count: float = 0.0
        for account in self.accounts:
            if account is CreditAccount:
                count += account.balance
            elif account is DebitAccount:
                count -= account.balance
        if not count == 0.0:
            print("Opps, the initial accounts are not balanced. Please check the data.")
            for account in self.accounts:
                os.remove(account.filePath)
            self.accounts.clear()
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
                command:Command = Command("create-account",{"accountType":accountType,"name":transaction.debitAccountName})
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
        if command.opt == "initialize-accounts":
            filePath = Path(command.args["filePath"])
            accountsInfo: pandas.DataFrame = pandas.read_csv(filePath)
            self.initAccounts(accountsInfo)

        elif command.opt == "create-account":
            accountType: AccountType = accountTypeConvert(command.args["accountType"])
            name: str = command.args["name"]
            self.createAccount(accountType,name,0.0)

        elif command.opt == "transaction":
            date: datetime = datetime.strptime(command.args["date"],"%Y-%m-%d")
            abstract: str = command.args["abstract"]
            creditAccountName: str = command.args["credit"]
            debitAccountName: str = command.args["debit"]
            amount: float = float(command.args["amount"])
            transaction = Transaction(len(self.transactions), date, abstract, creditAccountName, debitAccountName, amount)
            self.handleTransaction(transaction)

        elif command.opt == "file-transactions":
            filePath = Path(command.args["filePath"])
            transactionsInfo: pandas.DataFrame = pandas.read_csv(filePath)
            for index, row in transactionsInfo:
                date: datetime = datetime.strptime(row["date"],"%Y-%m-%d")
                abstract: str = row["abstract"]
                creditAccountName: str = row["credit"]
                debitAccountName: str = row["debit"]
                amount: float = float(row["amount"])
                transaction = Transaction(len(self.transactions),date,abstract,creditAccountName,debitAccountName,amount)
                self.handleTransaction(transaction)

        elif command.opt == "report":
            self.formReport()
            self.displayReport()

        elif command.opt == "analyze":
            self.analyzeData()

        elif command.opt == "help":
            print("This is a help message.")
            #todo: print help message

        return