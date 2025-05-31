from pandas import DataFrame

from src.object.Account import AccountType
from src.object.Company import Company
from pathlib import Path
import pandas


class Report:
    assetLiabilityPath: Path
    profitPath: Path

    def __init__(self):
        self.assetLiabilityPath = Path("data/reports/资产负债表")
        self.profitPath = Path("data/reports/利润表")

    def saveALReport(self, assets: DataFrame, liabilities: DataFrame, ownersEquity: DataFrame):
        with open(self.assetLiabilityPath.with_suffix("/资产.csv"), "w+", newline="") as fp:
            assets.to_csv(fp, index=False)
        with open(self.assetLiabilityPath.with_suffix("/负债.csv"), "w+", newline="") as fp:
            liabilities.to_csv(fp, index=False)
        with open(self.assetLiabilityPath.with_suffix("/所有者权益.csv"),"w+",newline="") as fp:
            ownersEquity.to_csv(fp, index=False)

    def saveProfitReport(self, revenue: DataFrame, expenses: DataFrame):
        with open(self.profitPath.with_suffix("/收入.csv"), "w+", newline="") as fp:
            revenue.to_csv(fp, index=False)
        with open(self.profitPath.with_suffix("/费用.csv"), "w+", newline="") as fp:
            expenses.to_csv(fp, index=False)


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
        #form report
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
