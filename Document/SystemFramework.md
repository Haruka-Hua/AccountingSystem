## 系统架构设计

### 1. 输入层（用户交互）
```python
class CommandLine:
    """
    负责读取用户命令行输入，解析命令和参数，生成 Command 对象。
    """
    def getNewCommand(self, message: str) -> Command: ...
    def readLine(self, message: str): ...
    def parseLine(self): ...
    def createCommand(self) -> Command: ...

class Command:
    """
    封装用户输入的操作类型（opt）和参数（args）。
    """
    def __init__(self, opt: str, args: dict): ...
```
### 2. 逻辑层（业务逻辑）
```python
class Company:
    """
    公司类，管理所有账户、分录、报表和分析。
    """
    def __init__(self, name: str): ...
    def initAccounts(self, accountInfo: DataFrame) -> bool: ...
    def createAccount(self, accountType: AccountType, name: str, initialBalance: float): ...
    def handleTransaction(self, transaction: Transaction): ...
    def formReport(self): ...
    def displayReport(self): ...
    def analyzeData(self): ...
    def executeCommand(self, command: Command): ...

class Account(ABC):
    """
    抽象账户类，定义账户类型、名称、余额、文件路径及分录处理接口。
    """
    @abstractmethod
    def handleDebitTransaction(self, transaction: Transaction): ...
    @abstractmethod
    def handleCreditTransaction(self, transaction: Transaction): ...

class DebitAccount(Account):
    """
    借方账户，贷方增加余额，借方减少余额。
    """
    def handleDebitTransaction(self, transaction: Transaction): ...
    def handleCreditTransaction(self, transaction: Transaction): ...

class CreditAccount(Account):
    """
    贷方账户，借方增加余额，贷方减少余额。
    """
    def handleDebitTransaction(self, transaction: Transaction): ...
    def handleCreditTransaction(self, transaction: Transaction): ...

class Transaction:
    """
    会计分录，包含序号、日期、摘要、借贷账户及金额。
    """
    def __init__(self, index: int, date: datetime, abstract: str, debitAccountName: str, 
                 creditAccountName: str, amount: float): ...
    def getTransactionInfo(self) -> dict: ...

class Reporter:
    """
    负责生成和展示报表。
    """
    def formReport(self): ...
    def displayReport(self): ...

class Report:
    """
    存储报表文件路径，负责保存报表到 CSV。
    """
    def saveALReport(self, assets: DataFrame, liabilities: DataFrame, ownersEquity: DataFrame): ...
    def saveProfitReport(self, revenue: DataFrame, expenses: DataFrame): ...

class Analyzer:
    """
    财务分析与可视化，生成饼图展示资产、负债、收入、费用结构。
    """
    def analyze(self): ...
```
### 数据层（存储结构）
账户数据、报表均以 CSV 文件存储，目录结构如下：
```
/data/
    ├── accounts/
    │     ├── 现金.csv
    │     ├── 银行存款.csv
    │     └── ...
    └── reports/
          ├── 资产负债表/
          │     ├── 资产.csv
          │     ├── 负债.csv
          │     └── 所有者权益.csv
          └── 利润表/
                ├── 收入.csv
                └── 费用.csv
```