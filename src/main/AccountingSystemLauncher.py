from src.object.Company import Company
from src.userInterface.CommandLine import CommandLine,Command

def main():
    cl = CommandLine()
    companyName = input("Name your company: ")
    company = Company(companyName)

    #initialize accounts
    print("Welcome to the Accounting System!")
    print("Firstly let's initialize your accounts. We will use a csv file to do this.")
    initialAccountPath:str = input("Please provide the file path of the csv file containing your accounts information: ")
    cl.line = f"initialize-accounts {initialAccountPath}"
    cl.parseLine()
    command: Command = cl.createCommand()
    company.executeCommand(command)

    print("Accounts initialized successfully! Now you can start operating your accounts.")
    print("You can add transactions, form reports, analyze data, and more.")
    print("Type 'help' for available commands.")

    #main loop
    while True:
        command: Command = cl.getNewCommand("Please enter a command: ")
        if command is None:
            continue
        if command.opt == "quit":
            break
        company.executeCommand(command)
        print("Command executed successfully!")