from src.object.Account import *
from src.object.Transaction import *
from src.userInterface.CommandLine import *
import pandas as pd
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

    def initAccounts(self,accountInfo: pd.DataFrame)->bool:
        for index, row in accountInfo.iterrows():
            accountType: AccountType = accountTypeConvert(row["accountType"])
            name: str = row["name"]
            initialBalance: float = float(row["initialBalance"])
            self.createAccount(accountType, name, initialBalance)
        #check balance
        count: float = 0.0
        for account in self.accounts.values():
            if isinstance(account, DebitAccount):
                count += account.balance
            elif isinstance(account, CreditAccount):
                count -= account.balance
        if count != 0.0:
            print("Opps, the initial accounts are not balanced. Please check the data.")
            for account in self.accounts.values():
                os.remove(account.filePath)
            self.accounts.clear()
            return False
        return True

    def createAccount(self, accountType: AccountType, name: str, initialBalance: float):
        if name in self.accounts:
            print(f"Account {name} already exists. Please choose a different name.")
            return
        if accountType == AccountType.ASSET or accountType == AccountType.PROFIT or accountType == AccountType.EXPENSE:
            self.accounts[name] = DebitAccount(accountType, name, initialBalance)
        elif accountType == AccountType.LIABILITY or accountType == AccountType.OWNERS_EQUITY or accountType == AccountType.REVENUE:
            self.accounts[name] = CreditAccount(accountType, name, initialBalance)
        else:
            raise ValueError(f"Invalid account type: {accountType}. Please choose a valid account type.")

    def addTransaction(self, transaction: Transaction):
        self.transactions.append(transaction)

    def checkTransactionAccounts(self,transaction:Transaction)->bool:
        if transaction.debitAccountName not in self.accounts:
            ans = input(f"{transaction.debitAccountName} does not exist. Do you want to create it?(Y/N)")
            if ans == "Y":
                while True:
                    accountType: str = input("Type of the account: ")
                    try:
                        command:Command = Command("create-account",{"accountType":accountType,"name":transaction.debitAccountName})
                        self.executeCommand(command)
                        return True
                    except ValueError as e:
                        print(e)
                        continue
            else:
                return False
        if transaction.creditAccountName not in self.accounts:
            ans = input(f"{transaction.creditAccountName} does not exist. Do you want to create it?(Y/N)")
            if ans == "Y":
                while True:
                    accountType: str = input("Type of the account: ")
                    try:
                        command:Command = Command("create-account",{"accountType":accountType,"name":transaction.creditAccountName})
                        self.executeCommand(command)
                        return True
                    except ValueError as e:
                        print(e)
                        continue
            else:
                return False
        return True

    def checkNullData(self,transaction)->bool:
        return ((not transaction.date is None) and (not transaction.debitAccountName is None)
            and (not transaction.creditAccountName is None) and (not transaction.amount is None))

    def handleTransaction(self, transaction: Transaction):
        if  self.checkNullData(transaction) and self.checkTransactionAccounts(transaction):
            debitSide:Account = self.accounts[transaction.debitAccountName]
            creditSide:Account = self.accounts[transaction.creditAccountName]
            debitSide.handleDebitTransaction(transaction)
            creditSide.handleCreditTransaction(transaction)
            self.addTransaction(transaction)
        else:
            print("Invalid transaction! Try again!")

    def showAllTransactions(self):
        df = pd.DataFrame([t.getTransactionInfo() for t in self.transactions])
        if df.empty:
            print("No transactions currently.")
        else:
            pd.set_option('display.unicode.east_asian_width', True)  # 让中英文对齐
            pd.set_option('display.width', 120)  # 设置显示宽度
            print(df.to_string(index=False))

    def formReport(self):
        self.reporter.formReport()

    def displayReport(self):
        self.reporter.displayReport()

    def analyzeData(self):
        self.analyzer.analyze()

    def displayHelp(self):
        # print help message
        print("Available commands:")
        print("<create-account>: Create a new account. The initial balance will be set to 0.0.\n"
              "\tFormat: <create-account> <accountType> <name>")
        print("<transaction>: Add a new transaction.\n"
              "\tFormat: <transaction> <date> <abstract> <debitAccountName> <creditAccountName> <amount>")
        print("<file-transactions>: Add transactions from a CSV file.\n"
              "\tFormat: <file-transactions> <filePath>")
        print("<report>: Generate and display a report.\n"
              "\tFormat: <report>")
        print("<analyze>: Analyze the data. Pie charts will be displayed to illustrate the composition of accounts.\n"
              "\tFormat: <analyze>")
        print("<show-transactions>: Display all transactions.\n"
              "\tFormat: <show-transactions>")
        print("<help>: Print this help message.\n"
              "\tFormat: <help>")
        print("<quit>: Exit the program.\n"
              "\tFormat: <quit>")
        return

    def executeCommand(self,command:Command):
        if command is None:
            print("Invalid command. Please try again.")
            return
        if command.opt == "initialize-accounts":
            filePath = Path(command.args["filePath"])
            accountsInfo: pd.DataFrame = pd.read_csv(filePath)
            if not self.initAccounts(accountsInfo):
                raise ValueError("The initial accounts are not balanced. Please check the data.")

        elif command.opt == "create-account":
            accountType: AccountType = accountTypeConvert(command.args["accountType"])
            name: str = command.args["name"]
            self.createAccount(accountType,name,0.0)

        elif command.opt == "transaction":
            date: datetime = datetime.strptime(command.args["date"],"%Y-%m-%d")
            abstract: str = command.args["abstract"]
            debitAccountName: str = command.args["debit"]
            creditAccountName: str = command.args["credit"]
            amount: float = float(command.args["amount"])
            transaction = Transaction(len(self.transactions), date, abstract, debitAccountName, creditAccountName, amount)
            self.handleTransaction(transaction)

        elif command.opt == "file-transactions":
            filePath = Path(command.args["filePath"])
            transactionsInfo: pd.DataFrame = None
            try:
                transactionsInfo = pd.read_csv(filePath)
            except FileNotFoundError:
                print("Sorry, the file does not exist, please check your spelling.")
            print(transactionsInfo)
            for index,row in transactionsInfo.iterrows():
                date: datetime = datetime.strptime(row["date"],"%Y-%m-%d")
                abstract: str = row["abstract"]
                debitAccountName: str = row["debit"]
                creditAccountName: str = row["credit"]
                amount: float = float(row["amount"])
                transaction = Transaction(len(self.transactions),date,abstract,debitAccountName,creditAccountName,amount)
                self.handleTransaction(transaction)

        elif command.opt == "report":
            self.formReport()
            self.displayReport()

        elif command.opt == "analyze":
            self.analyzeData()

        elif command.opt == "show-transactions":
            self.showAllTransactions()

        elif command.opt == "help":
            self.displayHelp()
        return