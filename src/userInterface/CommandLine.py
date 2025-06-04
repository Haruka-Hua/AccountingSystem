class Command:
    opt: str
    args: dict
    def __init__(self,opt:str,args:dict):
        self.opt = opt
        self.args = args

class CommandLine:
    line:str
    opt:str
    args:list
    optionInfo:dict
    command:Command

    def __init__(self):
        self.str = ""
        self.opt = ""
        self.args = []
        self.command = None
        options = []
        optArgs = []
        #create options
        #initialize accounts
        options.append("initialize-accounts")
        optArgs.append(["filePath"])
        #create account
        options.append("create-account")
        optArgs.append(["accountType","name"])
        #add transaction
        options.append("transaction")
        optArgs.append(["date","abstract","debit","credit","amount"])
        #add transactions(from file)
        options.append("file-transactions")
        optArgs.append(["filePath"])
        #form report
        options.append("report")
        optArgs.append([])
        #analyze data
        options.append("analyze")
        optArgs.append([])
        #show transactions
        options.append("show-transactions")
        optArgs.append([])
        #quit system
        options.append("quit")
        optArgs.append([])
        #print help
        options.append("help")
        optArgs.append([])
        self.optionInfo = dict(zip(options, optArgs))

    def getNewCommand(self,message:str) -> Command:
        self.readLine(message)
        self.parseLine()
        if not self.opt in self.optionInfo:
            print(f"Invalid option: {self.opt}. Type 'help' for available commands.")
            return None
        return self.createCommand()

    def readLine(self,message:str):
        self.line:str = input(message)

    def parseLine(self):
        elements = self.line.split()
        self.opt = elements[0]
        self.args = elements[1:]

    def createCommand(self) -> Command:
        bindings = dict(zip(self.optionInfo[self.opt], self.args))
        return Command(self.opt,bindings)
