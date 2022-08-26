from db.database import get_last_account_number, conn, cur
import re
class Account():
    
    def __init__(self):
        
        self.__account_number = None
        self.__name = None
        self.__last_name = None
        self.__client_id = None
        self.__birth_date = None
        self.__address = None
        self.__balance = 0

    @property
    def account_number(self):
        return self.__account_number
    
    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, name: str):
        self.__name = name

    @property
    def last_name(self):
        return self.__last_name
    
    @last_name.setter
    def last_name(self, last_name: str):
        self.__last_name = last_name
    
    @property
    def client_id(self):
        return self.__client_id
    
    @client_id.setter
    def client_id(self, client_id: str):
        self.__client_id = client_id
    
    @property
    def birth_date(self):
        return self.__birth_date

    @birth_date.setter
    def birth_date(self, birth_date: str):
        self.__birth_date = birth_date
    
    @property
    def address(self):
        return self.__address
    
    @address.setter
    def address(self, address: str):
        self.__address = address

    @property
    def balance(self):
        return self.__balance

    @balance.setter
    def balance(self, balance: float):
        self.__balance = balance

    def load_account_from_db(self, account_number: int):
        
        cur.execute('''
        SELECT * FROM account
        WHERE account_number = {}'''.format(account_number))

        results = cur.fetchone()

        self.__account_number = int(results['account_number'])
        self.__name = results['name']
        self.__last_name = results['last_name']
        self.__client_id = str(results['client_id'])
        self.__birth_date = results['birth_date']
        self.__address = results['address']
        self.__balance = float(results['balance'])
        
        return self
    
    def insert_into_db(self):
        cur.execute('''INSERT INTO account VALUES({}, '{}', '{}', '{}', '{}', '{}', {})'''\
                       .format(self.__account_number,self.__name, self.__last_name,\
                       self.__client_id, self.__birth_date, self.__address, self.__balance))
        
        conn.commit()
    
    def remove_from_db(self):
        cur.execute('''DELETE FROM account WHERE account_number IS {}'''\
            .format(self.__account_number))
        
        conn.commit()

    def update_db(self, column: str, new_value: tuple[int, float, str]):
        if column != 'account_number':
            cur.execute('''UPDATE account SET '{}' = '{}' WHERE account_number IS {}'''\
                .format(column, new_value, self.__account_number))
            
            conn.commit()
                
        else:
            print("\nAccount number can't be changed")
    

    def create_account(self):
    
        registration_attributes = {'name':'First Name', 'last_name': 'Last Name',\
             'client_id': 'Client ID Number (CPF with 11 digits)', 'birth_date': 'Date of Birth (yyyy-mm-dd)',\
                'address':'Full Address: Street, number, city, state'}

        self.__account_number = get_last_account_number()

        for attribute, attribute_description in registration_attributes.items():
            try:
                attribute_value = input(f"\nType the {attribute_description} of the account's owner ")
                
                while attribute_value == '':
                    print(f'\n{attribute_description} is empty, please type a valid value')
                    attribute_value = input(f"\nType the {attribute_description} of the account's owner ")
            
            except ValueError:
                print('Invalid attribute value')
            
            else:
                if attribute == 'client_id':
                    while not bool(re.match('[0-9]{11}$',attribute_value)):
                        print('Client ID must be an 11 digit number')
                        attribute_value = input(f"\nType the {attribute_description} of the account's owner ")
                    
                elif attribute == 'birth_date':
                    while not bool(re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}$',attribute_value)):
                        print('Date of Birth must be in the following format (yyyy-mm-dd')
                        attribute_value = input(f"\nType the {attribute_description} of the account's owner ")
                else:
                    setattr(self, attribute, attribute_value)

        self.insert_into_db()


    def deposit_money(self):
        try:
            account_for_deposit = int(input('Type the number of the destination account for the deposit '))
        
        except ValueError:
            print('\nInvalid account number')
            self.deposit_money()

        else:
            if Account.check_if_account_exists(account_for_deposit):
                self.load_account_from_db(account_for_deposit)
                
                print(f'\nAccount number to receive deposited {account_for_deposit}')
                
                try:
                    value = float(input('\nInsert deposit Value '))
                
                except ValueError:
                    print('\nInvalid Value, numeric value expected')
                    
                else:
                    if value <= 0:
                        print('\nInvalid value, positive value expected')
                    
                    else:
                        self.__balance += value
                        
                        self.update_db('balance', self.__balance)
                        
                        print(f'\nDeposited of R${value} made successfully to Account {self.__account_number}!')
                        print(f"\nThe Balance of the account {self.__account_number} is now {self.balance}")

            else:
                print('\nThe account your trying to deposit is not registered')
                
                self.deposit_money()


    def withdraw_money(self):
        try:
            account_to_withdraw = int(input('Type the number of the account to be drawn '))
        
        except ValueError:
            print('\nInvalid account number')
            self.withdraw_money()

        else:
            if Account.check_if_account_exists(account_to_withdraw):
                self.load_account_from_db(account_to_withdraw)
                
                print(f'\nAccount number to be drawn {account_to_withdraw}')
                
                try:
                    value = float(input('\nInsert withdraw value '))
                
                except ValueError:
                    print('\nInvalid Value, numeric value expected')
                    
                else:
                    if value <= 0:
                        print('\nInvalid value, positive value expected')

                    else:
                        if Account.check_sufficient_funds(account_to_withdraw, value):
                            self.__balance -= value
                            
                            self.update_db('balance', self.__balance)
                            
                            print(f'\nWithdraw of R${value} made successfully to Account {self.__account_number}!')
                            print(f"\nThe Balance of the account {self.__account_number} is now {self.balance}")

            else:
                print('\nThe account your trying to deposit is not registered')
                
                self.withdraw_money()
    
    def transfer_money(self):
        try:
            source_account_number = int(input(f'\nType the source account number '))
            target_account_number = int(input(f'\nType the target account number '))

        except ValueError as err:
                print(f'\n{err} Invalid account number')
                self.transfer_money()

        else:
            if Account.check_if_account_exists(source_account_number):
                if Account.check_if_account_exists(target_account_number):
                    self.load_account_from_db(source_account_number)
                    
                    target_account = Account()
                    target_account.load_account_from_db(target_account_number)
                
                    print(f'\nSource Account number {self.account_number}')
                    print(f'\nTarget Account number {target_account.account_number}')
                    
                    try:
                        transaction_value = float(input('Type the value to be transferred '))
                    
                    except ValueError:
                        print('\nInvalid Value, numeric value expected')
                    
                    else:
                        if Account.check_sufficient_funds(self.account_number, transaction_value):
                            self.balance -= transaction_value
                            self.update_db('balance', self.balance)

                            target_account.balance += transaction_value
                            target_account.update_db('balance', target_account.balance)

                            print(f'Transaction concluded successfully!')
                            print(f'{self.balance}')
                            print(target_account.balance)

                else:
                    print(f'\nTarget account {target_account} is not registered')    
            else:
                print(f'\nSource account {self.account_number} is not registered')

    @staticmethod
    def check_if_account_exists(account_number_to_be_check: int) -> bool:
            cur.execute('''SELECT * FROM account WHERE account_number = {}'''.format(account_number_to_be_check))
                
            res = cur.fetchone()

            if res != None:
                return True
            
            else:
                return False
    @staticmethod
    def check_sufficient_funds(account_number_to_be_check: int, value_to_be_check: float) -> bool:
            cur.execute('''SELECT * FROM account WHERE account_number = {}'''.format(account_number_to_be_check))
                
            res = cur.fetchone()

            if res['balance'] <= value_to_be_check:
                print('\nInsufficient funds')
            
            else:
                return True