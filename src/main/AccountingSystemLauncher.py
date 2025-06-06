from src.object.Company import Company
from src.userInterface.CommandLine import CommandLine,Command

def main():
    cl = CommandLine()
    companyName = input("Name your company:\n>>> ")
    company = Company(companyName)

    #initialize accounts
    print("Welcome to the Accounting System!")
    print("Firstly let's initialize your accounts. We will use a csv file to do this.")
    while True:
        try:
            initialAccountPath = input("Please enter the path to your initial accounts csv file:\n>>> ")
            cl.line = f"initialize-accounts {initialAccountPath}"
            cl.parseLine()
            command: Command = cl.createCommand()
            company.executeCommand(command)
            break
        except FileNotFoundError:
            print("File not found. Please check the path and try again.")
            continue
        #if initial balance is not balanced
        except ValueError as e:
            print(e)
            continue

    print("Accounts initialized successfully! Now you can start operating your accounts.")
    print("You can add transactions, form reports, analyze data, and more.")
    print("Type 'help' for available commands.")

    #main loop
    while True:
        command: Command = cl.getNewCommand("Please enter a command:\n>>> ")
        if command is None:
            continue
        if command.opt == "quit":
            break
        try:
            company.executeCommand(command)
            print(f"Command <{command.opt}> executed successfully!")
        except Exception:
            print("Opps, something went wrong! Please check your command (arguments and files) and try again.")

if __name__ == "__main__":
    main()