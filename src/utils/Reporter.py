import pandas as pd
from pandas import DataFrame
from src.object.Account import AccountType, prj_path
from pathlib import Path
import os
import pandas

class Report:
    assetLiabilityPath: Path
    profitPath: Path

    def __init__(self):
        self.assetLiabilityPath = prj_path.joinpath(Path("data/reports/资产负债表"))
        self.profitPath = prj_path.joinpath(Path("data/reports/利润表"))

    def saveALReport(self, assets: DataFrame, liabilities: DataFrame, ownersEquity: DataFrame):
        with open(self.assetLiabilityPath.joinpath(Path("资产.csv")), "w+", newline="") as fp:
            assets.to_csv(fp, index=False)
        with open(self.assetLiabilityPath.joinpath(Path("负债.csv")), "w+", newline="") as fp:
            liabilities.to_csv(fp, index=False)
        with open(self.assetLiabilityPath.joinpath(Path("所有者权益.csv")),"w+",newline="") as fp:
            ownersEquity.to_csv(fp, index=False)

    def saveProfitReport(self, revenue: DataFrame, expenses: DataFrame):
        with open(self.profitPath.joinpath(Path("收入.csv")), "w+", newline="") as fp:
            revenue.to_csv(fp, index=False)
        with open(self.profitPath.joinpath(Path("费用.csv")), "w+", newline="") as fp:
            expenses.to_csv(fp, index=False)


class Reporter:
    assets: DataFrame
    liabilities: DataFrame
    ownersEquity: DataFrame
    revenues: DataFrame
    expenses: DataFrame


    def __init__(self, company):
        from src.object.Company import Company
        self.company = company
        self.assets = DataFrame(columns = ["accountName", "balance"])
        self.liabilities = DataFrame(columns = ["accountName", "balance"])
        self.ownersEquity = DataFrame(columns = ["accountName", "balance"])
        self.revenues = DataFrame(columns = ["accountName", "balance"])
        self.expenses = DataFrame(columns = ["accountName", "balance"])

    def formReport(self):
        #clear previous reports
        self.assets = DataFrame(columns=["accountName", "balance"])
        self.liabilities = DataFrame(columns=["accountName", "balance"])
        self.ownersEquity = DataFrame(columns=["accountName", "balance"])
        self.expenses = DataFrame(columns=["accountName", "balance"])
        self.revenues = DataFrame(columns=["accountName", "balance"])
        #delete previous report files
        for file in os.listdir(self.company.report.assetLiabilityPath):
            filePath = self.company.report.assetLiabilityPath.joinpath(Path(file))
            if os.path.isfile(filePath):
                os.remove(filePath)
        #form report
        for account in self.company.accounts.values():
            newRow = pd.DataFrame([{"accountName": account.name, "balance": account.balance}])
            if account.accountType == AccountType.ASSET:
                self.assets = pd.concat([self.assets,newRow], ignore_index=True)
            elif account.accountType == AccountType.LIABILITY:
                self.liabilities = pd.concat([self.liabilities,newRow], ignore_index=True)
            elif account.accountType == AccountType.OWNERS_EQUITY:
                self.ownersEquity = pd.concat([self.ownersEquity,newRow], ignore_index=True)
            elif account.accountType == AccountType.REVENUE:
                self.revenues = pd.concat([self.revenues,newRow], ignore_index=True)
            elif account.accountType == AccountType.EXPENSE:
                self.expenses = pd.concat([self.expenses,newRow], ignore_index=True)
            else:
                print(f"Invalid account type for {account.name}. Skipping.")
        #save reports to csv files
        self.company.report.saveALReport(self.assets, self.liabilities, self.ownersEquity)
        self.company.report.saveProfitReport(self.revenues, self.expenses)

        return

    def displayReport(self):
        #display report
        print("-----------资产负债表-----------")
        print("Assets:")
        print(self.assets)
        print("Total Assets:", self.assets["balance"].sum())
        print("Liabilities:")
        print(self.liabilities)
        print("Total Liabilities:", self.liabilities["balance"].sum())
        print("Owner's Equity:")
        print(self.ownersEquity)
        print("Total Owner's Equity:", self.ownersEquity["balance"].sum())
        print("Total Liabilities and Owner's Equity:", self.liabilities["balance"].sum() + self.ownersEquity["balance"].sum())

        print("-----------利润表-----------")
        print("Revenues:")
        print(self.revenues)
        print("Total Revenues:", self.revenues["balance"].sum())
        print("Expenses:")
        print(self.expenses)
        print("Total Expenses:", self.expenses["balance"].sum())
        print("Net Profit:", self.revenues["balance"].sum() - self.expenses["balance"].sum())

        return
