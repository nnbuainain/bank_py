from models.account import Account
from db.database import connect_or_create_bank_db, list_accounts

def menu() -> bool:
        print("\nWelcome to the bank\n")
        print("1) Create a new account")
        print("2) Deposit money into an account")
        print("3) Withdraw money from an account")
        print("4) Transfer money between accounts")
        print("5) See list of accounts")
        print("6) Exit")

def main() -> bool:
    
    option = None

    conn, cur = connect_or_create_bank_db()

    while option != 6:
        menu()

        try:
            choice = input("\nEnter your choice: ")
        
        except ValueError:
            print("\nInvalid option")
            menu()

        else:
            if choice == "1":
                acc = Account()
                
                acc.create_account()
                
                print(f'\nAccount {acc.account_number} created successfully')
                
                list_accounts()

            elif choice == "2":
                acc = Account()

                acc.deposit_money()
            
            elif choice == "3":
                acc = Account()
                
                acc.withdraw_money()
            
            elif choice == "4":
                acc = Account()

                acc.transfer_money()

            elif choice == "5":
                print('\n######## Showing list of accounts registered ########')
                list_accounts()
            
            elif choice == "6":
                print('\nExiting the app...')
                print('Goodbye!')
                
                return False
            
            else:
                print('\nInvalid choice, please type an option between 1 and 6')
                
                menu()


if __name__ == '__main__':
    main()