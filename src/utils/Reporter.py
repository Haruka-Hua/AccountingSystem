from src.object.Company import Company
from pathlib import Path


class Report:
    assetLiabilityPath: Path
    profitPath: Path

    def __init__(self):
        self.assetLiabilityPath = Path("data/reports/资产负债表.csv")
        self.profitPath = Path("data/reports/利润表.csv")


class Reporter:
    company: Company

    def __init__(self, company: Company):
        self.company = company

    def formReport(self):
        #todo: form report
        return

    def displayReport(self):
        #todo: display report
        return
