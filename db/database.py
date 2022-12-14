import sqlite3
import os.path

def connect_or_create_bank_db() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    conn = sqlite3.connect(os.path.realpath('./db/bank.db'))
    
    conn.row_factory = sqlite3.Row
    
    cur = conn.cursor() 

    create_db_script = ''' CREATE TABLE IF NOT EXISTS account (
                                    account_number      int PRIMARY KEY,
                                    name    varchar(40) NOT NULL,
                                    last_name    varchar(40) NOT NULL,
                                    client_id  varchar(11) NOT NULL,
                                    birth_date date NOT NULL,
                                    address varchar(40) NOT NULL,
                                    balance float(2) NOT NULL
                                    ) '''

    cur.execute(create_db_script)
    
    return conn, cur


def insert_into_db(account, conn, cur):
    cur.execute('''INSERT INTO account VALUES({}, '{}', '{}', '{}', '{}', '{}', {})'''\
                    .format(account.account_number,account.name, account.last_name,\
                    account.client_id, account.birth_date, account.address, account.balance))
    
    conn.commit()

# def remove_from_db(account, conn, cur):
#     cur.execute('''DELETE FROM account WHERE account_number IS {}'''\
#         .format(account.account_number))
    
#     conn.commit()

def update_db(account, column: str, new_value: tuple[int, float, str], conn, cur):
    if column != 'account_number':
        cur.execute('''UPDATE account SET '{}' = '{}' WHERE account_number IS {}'''\
            .format(column, new_value, account.account_number))
        
        conn.commit()
            
    else:
        print("\nAccount number can't be changed")


def get_last_account_number(conn, cur) -> int:
    
    cur.execute('''SELECT * FROM account ORDER BY account_number DESC LIMIT 1''')
    
    res = cur.fetchone()
    
    if res == None:
        return 0
    
    else: 
        return res['account_number']


def list_accounts(conn, cur):
    
    cur.execute('''SELECT * from account''')
    
    accounts = cur.fetchall()

    if accounts is not None:

        for account in accounts:
            
            print('\n##############################################################################')
            
            print(f"\nAccount Number: {account['account_number']}\t \
                      Account Owner: {account['name']} {account['last_name']}")
            
            print(f"Account Balance: ${account['balance']:.2f}")
            
            print('\n##############################################################################\n')
    else:
        print('The Database is currently empty')


def delete_db(conn, cur):
    file_path = './bank.db'
    
    if os.path.isfile(file_path):
        confirm_deletion = input("Are you sure you want to delete the database? \
                                        You won't be able to retrieve the information \
                                        in the future (Y/n) ")
        
        if confirm_deletion.upper() == 'Y':
            print("Database has been deleted")

            os.remove(file_path)
            
            conn.close() 
            
            cur.close()


def check_if_account_exists(account_number_to_be_check: int, conn, cur) -> bool:
        cur.execute('''SELECT * FROM account WHERE account_number = {}'''.format(account_number_to_be_check))
            
        res = cur.fetchone()

        if res != None:
            return True
        
        else:
            return False


def check_sufficient_funds(account_number_to_be_check: int, value_to_be_check: float, conn, cur) -> bool:
        cur.execute('''SELECT * FROM account WHERE account_number = {}'''.format(account_number_to_be_check))
            
        res = cur.fetchone()

        if res['balance'] <= value_to_be_check:
            print('\nInsufficient funds')
        
        else:
            return True