from Account import *
from Transaction import *
from src.utils.Analyzer import *
from src.utils.Reporter import *


class Company:
    name:str
    accounts:dict[str:Account]
    transactions:list[Transaction]
    analyzer: Analyzer
    reporter: Reporter
    report: Report

    def __init__(self,name:str):
        self.name = name
        #todo: initialize company
        return

    def createAccount(self):
        #todo
        return

    def handleTransaction(self,transaction:Transaction):
        #todo
        return

    def formReport(self):
        #todo
        return

    def displayReport(self):
        #todo
        return

    def analyzeData(self):
        #todo
        return