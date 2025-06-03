from pandas import DataFrame, read_csv
from pathlib import Path
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

class Analyzer:
    types = ["Assets", "Liabilities", "Owner's equities", "Revenues", "Expenses"]

    def __init__(self, company):
        from src.object.Company import Company
        self.company = company

    def analyzeSingleType(self,accType:str,typeInfo:DataFrame):
        typeInfo = typeInfo[typeInfo["balance"] != 0]  # Filter out zero balances
        labels = typeInfo["accountName"].tolist()
        balances = typeInfo["balance"].tolist()
        colors = plt.get_cmap('Set3').colors
        plt.figure(figsize=(10,8))
        patches, texts, autotexts = plt.pie(balances, colors=colors,autopct='%1.1f%%', startangle=90, pctdistance=1.1)
        plt.title(f"{accType} Composition", fontsize=16)
        plt.legend(patches,labels,loc='upper left', bbox_to_anchor=(0, 1))
        plt.axis('equal')
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