## 系统架构设计
### 1. 输入层
```
class CommandLine{
    String line;
    
    void readLine();
    Command parse();
}
class Command{
    String option;
    List args;
}
```
### 2. 逻辑层
```
class Company{
    String name;
    List accounts;
    String directory;
    List Transcation;
    Analyzer analyzer;
    Reporter reporter;
    Report report;
    
    void createAccount();
    void getAccount();
    void handleTranscation();
    void formReport();
    void displayReport();
    void analyzeData();
}
```
```
abstract class Account{
    AccountType accountType;
    String name;
    float balance;
    String filePath;
    
    abstract void handleTranscation();
}

class CreditAccount extends Account{
    void handleTranscation();
}

class DebitAccount extends Account{
    void handleTranscation();
}
```
```
class Transcation{
    int index;
    LocalDate date;
    String abstract;
    String creditAccount;
    String debitAccount;
    float amount;
}
```
```
class Reporter{
    Company company;
    
    void report();
}
class Report{
    String assetLiabilityPath;
    String profitPath;
}
```
```
class Analyzer{
    Company company;
    
    void analyze();
}
```
### 数据层
数据存储结构：
```
\company\
    ├──accounts/
        ├──银行存款.csv
        ├──应付账款.csv
        ......├──
    ├──reports
        ├──资产负债表.csv
        ├──利润表.csv
```