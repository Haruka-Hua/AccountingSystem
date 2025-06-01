from src.object.Account import *
from src.object.Transaction import *
from src.userInterface.CommandLine import *
import pandas
import os

from src.utils.Analyzer import Analyzer
from src.utils.Reporter import Report, Reporter


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
        self.analyzer = Analyzer(self)
        self.reporter = Reporter(self)
        self.report = Report()
        #clear the data directory
        dir_path = prj_path.joinpath(Path("data/accounts"))
        for filename in os.listdir(dir_path):
            filepath = dir_path.joinpath(Path(filename))
            if os.path.isfile(filepath):
                os.remove(filepath)

    def initAccounts(self,accountInfo: pandas.DataFrame)->bool:
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
        if count != 0.0:
            print("Opps, the initial accounts are not balanced. Please check the data.")
            for account in self.accounts:
                os.remove(account.filePath)
            self.accounts.clear()
            return False
        return True

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
        if command is None:
            print("Invalid command. Please try again.")
            return
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
            transactionsInfo: pandas.DataFrame = None
            try:
                transactionsInfo = pandas.read_csv(filePath)
            except FileNotFoundError:
                print("Sorry, the file does not exist, please check your spelling.")
            print(transactionsInfo)
            for index,row in transactionsInfo.iterrows():
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
            #print help message
            print("Available commands:")
            print("<create-account>: Create a new account. The initial balance will be set to 0.0.")
            print("<transaction>: Add a new transaction.")
            print("<file-transactions>: Add transactions from a CSV file.")
            print("<report>: Generate and display a report.")
            print("<analyze>: Analyze the data. Pie charts will be displayed to illustrate the composition of accounts.")
            print("<help>: Print this help message.")
            print("<quit>: Exit the program.")

        return