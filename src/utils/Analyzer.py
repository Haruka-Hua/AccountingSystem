from pandas import DataFrame, read_csv
from pathlib import Path
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

class Analyzer:
    types = ["Assets", "Liabilities", "Owner's equities", "Revenues", "Liabilities"]

    def __init__(self, company):
        from src.object.Company import Company
        self.company = company

    def analyzeSingleType(self,accType:str,typeInfo:DataFrame):
        labels = typeInfo["accountName"].tolist()
        balances = typeInfo["balance"].tolist()
        plt.figure(figsize=(10, 6))
        plt.pie(balances, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.axis("equal")
        plt.title(f"{accType} Composition")
        plt.show()
        return

    def analyze(self):
        #analyze data
        for accType in self.types:
            self.analyzeSingleType(accType,self.getTypeInfo(accType))
        return

    def getTypeInfo(self,accType:str)->DataFrame:
        if accType=="Assets":
            return read_csv(self.company.report.assetLiabilityPath.joinpath(Path("资产.csv")),encoding="GBK")
        elif accType == "Liabilities":
            return read_csv(self.company.report.assetLiabilityPath.joinpath(Path("负债.csv")),encoding="GBK")
        elif accType == "Owner's equities":
            return read_csv(self.company.report.assetLiabilityPath.joinpath(Path("所有者权益.csv")),encoding="GBK")
        elif accType == "Revenues":
            return read_csv(self.company.report.profitPath.joinpath(Path("收入.csv")),encoding="GBK")
        elif accType == "Expenses":
            return read_csv(self.company.report.profitPath.joinpath(Path("费用.csv")),encoding="GBK")