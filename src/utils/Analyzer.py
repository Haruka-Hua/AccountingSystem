from pandas import DataFrame, read_csv
from src.object.Company import Company
import matplotlib.pyplot as plt


class Analyzer:
    company: Company
    types = ["Assets", "Liabilities", "Owner's equities", "Revenues", "Liabilities"]

    def __init__(self, company: Company):
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
            return read_csv(self.company.report.assetLiabilityPath.with_suffix("/资产.csv"))
        elif accType == "Liabilities":
            return read_csv(self.company.report.assetLiabilityPath.with_suffix("/负债.csv"))
        elif accType == "Owner's equities":
            return read_csv(self.company.report.assetLiabilityPath.with_suffix("/所有者权益.csv"))
        elif accType == "Revenues":
            return read_csv(self.company.report.profitPath.with_suffix("/收入.csv"))
        elif accType == "Expenses":
            return read_csv(self.company.report.profitPath.with_suffix("/费用.csv"))