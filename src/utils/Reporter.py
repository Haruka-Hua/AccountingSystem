from pandas import DataFrame

from src.object.Account import AccountType
from src.object.Company import Company
from pathlib import Path
import pandas


class Report:
    assetLiabilityPath: Path
    profitPath: Path

    def __init__(self):
        self.assetLiabilityPath = Path("data/reports/资产负债表.csv")
        self.profitPath = Path("data/reports/利润表.csv")

    def saveALReport(self, assets: DataFrame, liabilities: DataFrame, ownersEquity: DataFrame):
        #todo: save asset liability report
        return

    def saveProfitReport(self, revenue: DataFrame, expenses: DataFrame):
        #todo: save profit report
        return


class Reporter:
    company: Company
    assets: DataFrame
    liabilities: DataFrame
    ownersEquity: DataFrame
    revenues: DataFrame
    expenses: DataFrame


    def __init__(self, company: Company):
        self.company = company
        self.assets = DataFrame(columns = ["accountName", "balance"])
        self.liabilities = DataFrame(columns = ["accountName", "balance"])
        self.ownersEquity = DataFrame(columns = ["accountName", "balance"])
        self.revenues = DataFrame(columns = ["accountName", "balance"])
        self.expenses = DataFrame(columns = ["accountName", "balance"])


    def formReport(self):
        #todo: form report
        for account in self.company.accounts:
            if account.acccountType == AccountType.ASSET:
                self.assets.append({"accountName": account.name, "balance": account.balance})
            elif account.accountType == AccountType.LIABILITY:
                self.liabilities.append({"accountName": account.name, "balance": account.balance})
            elif account.accountType == AccountType.OWNERS_EQUITY:
                self.ownersEquity.append({"accountName": account.name, "balance": account.balance})
            elif account.accountType == AccountType.REVENUE:
                self.revenues.append({"accountName": account.name, "balance": account.balance})
            elif account.accountType == AccountType.EXPENSE:
                self.expenses.append({"accountName": account.name, "balance": account.balance})
            else:
                print(f"Invalid account type for {account.name}. Skipping.")
        #todo: save reports to csv files
        self.company.report.saveALReport(self.assets, self.liabilities, self.ownersEquity)
        self.company.report.saveProfitReport(self.revenues, self.expenses)

        return

    def displayReport(self):
        #todo: display report
        return
