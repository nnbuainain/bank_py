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

conn, cur = connect_or_create_bank_db()

def get_last_account_number() -> int:
    global conn, cur
    
    cur.execute('''SELECT * FROM account ORDER BY account_number DESC LIMIT 1''')
    
    res = cur.fetchone()
    
    if res == None:
        return 0
    
    else: 
        return res['account_number']

def list_accounts():
    global conn, cur
    
    cur.execute('''SELECT * from account''')
    
    accounts = cur.fetchall()

    if accounts is not None:

        for account in accounts:
            
            print('\n##############################################################################')
            
            print(f"\nAccount Number: {account['account_number']}\t \
                      Account Owner: {account['name']} {account['last_name']}")
            
            print(f"Account Balance: {account['balance']}")
            
            print('\n##############################################################################\n')
    else:
        print('The Database is currently empty')

def delete_db():
    file_path = './bank.db'
    
    if os.path.isfile(file_path):
        confirm_deletion = input("Are you sure you want to delete the database? \
                                        You won't be able to retrieve the information \
                                        in the future (Y/n)")
        
        if confirm_deletion.upper() == 'Y':
            print("Database has been deleted")

            os.remove(file_path)
            
            conn.close() 
            
            cur.close()