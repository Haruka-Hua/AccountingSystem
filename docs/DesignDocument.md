## 会计系统-设计文档

### 1. 系统架构设计
- 架构模式：分层架构。
  - 输入层：命令行交互及文件读取。
  - 逻辑层：处理会计分录、更新账户、生成报表。
  - 数据层：使用CSV文件存储账户数据和报表。
- 技术栈
  - 语言：Python
  - 主要库：pandas、matplotlib
  - 数据存储：CSV 文件
  - 运行环境：命令行（CLI）
  - 主要依赖：标准库（如 csv、datetime、pathlib 等）

### 2. 模块设计
#### 2.1 交互模块
- 使用命令行实现数据输入、输出
- 命令及命令行类：
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
- 目前支持的命令：
```commandline
- <create-account>：创建新账户，初始余额为0.0。  
  格式：<create-account> <accountType> <name>
  
- <transaction>：添加一条新的会计分录。  
  格式：<transaction> <date> <abstract> <debitAccountName> <creditAccountName> <amount>

- <file-transactions>：从CSV文件批量导入会计分录。  
  格式：<file-transactions> <filePath>

- <report>：生成并显示报表。  
  格式：<report>

- <analyze>：进行财务分析，生成账户结构饼图。  
  格式：<analyze>

- <show-transactions>：显示所有已录入的会计分录。  
  格式：<show-transactions>

- <help>：显示帮助信息。  
  格式：<help>

- <quit>：退出程序。  
  格式：<quit>
```
#### 2.2 账户管理模块
- 以公司为单位管理账户
- 公司类：
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

```
- 账户分类：资产、负债、所有者权益、收入、费用、利润
- 账户类：
```python
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
```
- 使用分录传递业务信息
- 分录类：
```python
class Transaction:
    """
    会计分录，包含序号、日期、摘要、借贷账户及金额。
    """
    def __init__(self, index: int, date: datetime, abstract: str, debitAccountName: str, 
                 creditAccountName: str, amount: float): ...
    def getTransactionInfo(self) -> dict: ...

```
#### 2.3 报表生成模块
- 生成并打印以下报表： 
  - 资产-负债表：汇总所有资产、负债以及所有者权益账户的信息，生成.csv文件 
  - 利润表：汇总收入和费用的信息，产生利润，生成.csv文件
- 报告器类：
```python
class Reporter:
    """
    负责生成和展示报表。
    """
    def formReport(self): ...
    def displayReport(self): ...
```
- 报告类：
```python
class Report:
    """
    存储报表文件路径，负责保存报表到 CSV。
    """
    def saveALReport(self, assets: DataFrame, liabilities: DataFrame, ownersEquity: DataFrame): ...
    def saveProfitReport(self, revenue: DataFrame, expenses: DataFrame): ...
```
#### 2.4 财务分析模块
- 利用报表信息，分别获取资产、负债等账户类型的数据，用饼图展示结构
- 分析器类
```python
class Analyzer:
    """
    财务分析与可视化，生成饼图展示资产、负债、所有者权益、收入、费用结构。
    """
    def analyze(self): ...
```
#### 2.5 启动器模块
- 使用`AccountingSystemLauncher.py`中的main函数启动程序

### 3. 数据存储设计
- 账户数据、报表均以 CSV 文件存储，目录结构如下：
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
- 初始账户录入：使用CSV文件录入，格式如下
```
    name,accountType,initialBalance
    库存现金,资产,880
```
- 账户数据：使用三栏式记账法，具体形式如下
```
    No.,date,abstract,debit,credit,balance
    1,2023-10-02,购买设备,500,,500
```
- 会计分录：
  - 通过命令行录入，参数之间使用空格隔开（注意参数中不能含有空格）
```
    format:   <date> <abstract> <debitAccountName> <creditAccountName> <amount>
    example:  2023-10-02 购买设备 固定资产 银行存款 10000
```
  - 通过读取.csv文件录入，格式如下
```
    date,abstract,debit,credit,amount
    2024-4-1,收到达声厂上月所欠汽车修理费存入银行,银行存款,应收账款,1200
```