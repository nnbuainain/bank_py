"""An application that simulates a bank account management system.
The app initialize as offers the user the following options:
1) Create a new account
2) Withdraw money from an account
3) Deposit money to an account

4) Transfer money between accounts
5) See list of accounts
6) Exit"""

def menu() -> bool:
    print("Welcome to the bank")
    print("1) Create a new account")
    print("2) Withdraw money from an account")
    print("3) Deposit money to an account")
    print("4) Transfer money between accounts")
    print("5) See list of accounts")
    print("6) Exit")

    try:
        choice = input("Enter your choice: ")
        if choice == "1":
            create_account()
        elif choice == "2":
            withdraw_money()
        elif choice == "3":
            deposit_money()
        elif choice == "4":
            transfer_money()
        elif choice == "5":
            list_accounts_money()
        elif choice == "6":
            return False
    
    except ValueError:
        print("Invalid option")
        menu()
    
    else:
        print("Invalid choice")
        menu()

def main() -> bool:
    menu()

if __name__ == '__main__':
    main()