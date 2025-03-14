import time as t # Fo use method sleep()
import os # To clean console
import psycopg2 # For work PGAdmin and SQL
from datetime import datetime # To check the entered date
import pandas as pd # For work with graph and analys
import matplotlib.pyplot as plt # To draw a graph

def clearConsole():
    os.system('cls')

def authorizationUser():
    conn = psycopg2.connect(
        dbname='-',    
        user='postgres',  
        password='-',  
        host='localhost',          
        port='5432'                
    )

    cur = conn.cursor()
    nickname = input("Input your nickname: ")
    password = input("Input your password: ")

    query = """
    SELECT EXISTS(
        SELECT 1 FROM Users 
        WHERE user_nickname = %s AND user_password = %s
    );
    """

    cur.execute(query, (nickname, password))
    exists = cur.fetchone()[0]

    if exists:
        print(f"Successfully authorization, {nickname}!"), mainMenuUser(nickname)
    else:
        print("Incorrect nickname or password."), t.sleep(5), clearConsole(), authorizationUser()

    cur.close()
    conn.close()

def mainMenuUser(nickname): 
    print(f'Welcome to system, {nickname}, what we will do?')
    print('1 - Enter expenses')
    print('2 - Enter income')
    print('3 - check all your actions')
    print('4 - check certain actions')
    choise = input('Your choise: ')
    if choise == '1':
        enterExpenses(nickname)
    elif choise == '2':
        enterIncome(nickname)
    elif choise == '3':
        outputAllActions(nickname)
    elif choise == '4':
        menuChecksWithConditions(nickname)
    else:
        print('Incorrect input! Try again!'), t.sleep(4), clearConsole(), mainMenuUser(nickname)
def menuChecksWithConditions(nickname):
    print('\n1 - output all your expenses')
    print('2 - output all your income')
    print('3 - select by amount')
    print('4 - select be date')
    print('5 - select by description')
    choise = input('Your choise: ')
    if choise == '1':
        outputAllExpenses(nickname)
    elif choise == '2':
        outputAllIncome(nickname)
    elif choise == '3':
        outputSelectByAmount(nickname)
    elif choise == '4':
        outputSelectByDate(nickname)
    elif choise == '5':
        outputSelectByDescription(nickname)
    else:
        print('Incorrect input! Try again!'), t.sleep(4), clearConsole(), menuChecksWithConditions(nickname)
def menuVisualisation(nickname):
    print('1 - visualization of expenses')
    print('2 - visualization of incomes')
    choise = input('Your choise: ')
    if choise == '1':
        visualizationExpenses(nickname)
    elif choise == '2':
        visualizationIncomes(nickname)
    else:
        print('Incorrect input! Try again!'), t.sleep(4), clearConsole(), menuVisualisation(nickname)

def enterExpenses(nickname):
    try:
        expenses = int(input('Input summ: '))
    except ValueError: 
        print('Incorrect input of summ! Try again!'), t.sleep(4), clearConsole(), enterExpenses(nickname)

    date = input("Enter the date of expenses in year-month-day format (YYYY-MM-DD): ")
    is_valid, parsed_date = check_date(date)
    if is_valid:
        description = input('Input description of expenses (up to 1000 characters): ')
        if len(description) < 1000:
            try:
                connection = psycopg2.connect(
                    dbname='-',    
                    user='postgres',  
                    password='-',  
                    host='localhost',          
                    port='5432'     
                )

                cursor = connection.cursor()
                insert_query = """
                INSERT INTO ExpensesOfUser (expensesofuser_summ, expensesofuser_dateExpenses, expensesofuser_description, user_nickname)
                VALUES (%s, %s, %s, %s);
                """

                cursor.execute(insert_query, (expenses, parsed_date, description, nickname))
                connection.commit()
                print('Recording successful!')

            except (Exception, psycopg2.DatabaseError) as error:
                print("Error with DB! ", error)
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
        else:
            print('Character limit exceeded! Try again!'), t.sleep(4), clearConsole(), enterExpenses(nickname) 
    else:
        print("Inputed date isn't correct."), t.sleep(4), clearConsole(), enterExpenses(nickname)

    pressEnter = input('\nPress ENTER to return at main menu')
    clearConsole(), mainMenuUser(nickname)
def enterIncome(nickname):
    try:
        income = int(input('Input summ: '))
    except ValueError: 
        print('Incorrect input of summ! Try again!'), t.sleep(4), clearConsole(), enterIncome(nickname)

    date = input("Enter the date of income in year-month-day format (YYYY-MM-DD): ")
    is_valid, parsed_date = check_date(date)
    if is_valid:
        description = input('Input description of income (up to 1000 characters): ')
        if len(description) < 1000:
            try:
                connection = psycopg2.connect(
                    dbname='-',    
                    user='postgres',  
                    password='-',  
                    host='localhost',          
                    port='5432'     
                )

                cursor = connection.cursor()
                insert_query = """
                INSERT INTO IncomeOfUser (incomeofuser_summ, incomeofuser_dateIncome, incomeofuser_description, user_nickname)
                VALUES (%s, %s, %s, %s);
                """

                cursor.execute(insert_query, (income, parsed_date, description, nickname))
                connection.commit()
                print('Recording successful!')

            except (Exception, psycopg2.DatabaseError) as error:
                print("Error with DB! ", error)
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
        else:
            print('Character limit exceeded! Try again!'), t.sleep(4), clearConsole(), enterIncome(nickname) 
    else:
        print("Inputed date isn't correct."), t.sleep(4), clearConsole(), enterIncome(nickname)

    pressEnter = input('\nPress ENTER to return at main menu')
    clearConsole(), mainMenuUser(nickname)

def check_date(input_date): # Function to check the date for correctness
    try:
        parsed_date = datetime.strptime(input_date, '%Y-%m-%d')
        return True, parsed_date
    except ValueError:
        return False, None

def outputAllActions(nickname):
    try:
        connection = psycopg2.connect(
            dbname='-',    
            user='postgres',  
            password='-',  
            host='localhost',          
            port='5432'                
        )
        
        cursor = connection.cursor()

        expenses_query = """
        SELECT expensesofuser_summ, expensesofuser_dateExpenses, expensesofuser_description
        FROM ExpensesOfUser
        WHERE user_nickname = %s;
        """
        cursor.execute(expenses_query, (nickname,))
        expenses_data = cursor.fetchall() 

        income_query = """
        SELECT incomeofuser_summ, incomeofuser_dateIncome, incomeofuser_description
        FROM IncomeOfUser
        WHERE user_nickname = %s;
        """
        cursor.execute(income_query, (nickname,))
        income_data = cursor.fetchall()

        print(f"Expenses for user {nickname}:")
        for row in expenses_data:
            print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

        print(f"\nIncome for user {nickname}:")
        for row in income_data:
            print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error with DB! ", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    pressEnter = input('\nPress ENTER to return at main menu')
    clearConsole(), mainMenuUser(nickname)
def outputAllExpenses(nickname):
    try:
        connection = psycopg2.connect(
            dbname='-',    
            user='postgres',  
            password='-',  
            host='localhost',          
            port='5432'                
        )
        
        cursor = connection.cursor()

        expenses_query = """
        SELECT expensesofuser_summ, expensesofuser_dateExpenses, expensesofuser_description
        FROM ExpensesOfUser
        WHERE user_nickname = %s;
        """
        cursor.execute(expenses_query, (nickname,))
        expenses_data = cursor.fetchall() 

        print(f"Expenses for user {nickname}:")
        for row in expenses_data:
            print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error with DB! ", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    pressEnter = input('\nPress ENTER to return at main menu')
    clearConsole(), mainMenuUser(nickname)
def outputAllIncome(nickname):
    try:
        connection = psycopg2.connect(
            dbname='-',    
            user='postgres',  
            password='-',  
            host='localhost',          
            port='5432'                
        )
        
        cursor = connection.cursor()
        income_query = """
        SELECT incomeofuser_summ, incomeofuser_dateIncome, incomeofuser_description
        FROM IncomeOfUser
        WHERE user_nickname = %s;
        """
        cursor.execute(income_query, (nickname,))
        income_data = cursor.fetchall()

        print(f"\nIncome for user {nickname}:")
        for row in income_data:
            print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

    except (Exception, psycopg2.DatabaseError) as error:
        print("Error with server! ", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    pressEnter = input('\nPress ENTER to return at main menu')
    clearConsole(), mainMenuUser(nickname)

def outputSelectByAmount(nickname):
    try:
        amount = int(input('Input amount: '))
    except ValueError: 
        print('Incorrect input of amount! Try again!'), t.sleep(4), clearConsole(), outputSelectByAmount(nickname)

    more = False
    less = False
    equal = False
    print('Enter condition:')
    print('Enter ">" to see transactions that exceed the amount you entered')
    print('Enter "<" to see transactions with a smaller amount than the amount you entered')
    print('Enter "=" to see transactions with the amount you entered')
    choiseSign = input('Your sign: ')
    if choiseSign == '>':
        more = True
    elif choiseSign == '<':
        less = True
    elif choiseSign == '=':
        equal = True
    else:
        print('Incorrect input! Try again!'), t.sleep(4), clearConsole(), outputSelectByAmount(nickname)        

    expenses = False
    income = False
    all = False
    print('You want to see expenses - enter 1, income - enter 2, all - enter 3')
    choiseOperation = input('Your choise: ')
    if choiseOperation == '1':
        expenses = True
    elif choiseOperation == '2':
        income = True
    elif choiseOperation == '3':
        all = True
    else:
        print('Incorrect input! Try again!'), t.sleep(4), clearConsole(), outputSelectByAmount(nickname)

    # Getting started with queries
    if more and expenses:
        try:
            connection = psycopg2.connect(
                dbname='-',    
                user='postgres',  
                password='-',  
                host='localhost',          
                port='5432'                
            )

            cursor = connection.cursor()

            expenses_query = """
                SELECT expensesofuser_summ, expensesofuser_dateExpenses, expensesofuser_description
                FROM ExpensesOfUser
                WHERE expensesofuser_summ > %s AND user_nickname = %s;
            """

            cursor.execute(expenses_query, (amount, nickname))
            expenses_data = cursor.fetchall()  

            print(f"\nExpenses greater than {amount}:")
            for row in expenses_data:
                print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error with DB! ", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        more = False
        expenses = False
        pressEnter = input('\nPress ENTER to return at main menu')
        clearConsole(), mainMenuUser(nickname)
    elif more and income:
        try:
            connection = psycopg2.connect(
                dbname='-',    
                user='postgres',  
                password='-',  
                host='localhost',          
                port='5432'                
            )

            cursor = connection.cursor()

            expenses_query = """
                SELECT incomeofuser_summ, incomeofuser_dateincome, incomeofuser_description
                FROM IncomeOfUser
                WHERE incomeofuser_summ > %s AND user_nickname = %s;
            """

            cursor.execute(expenses_query, (amount, nickname))
            expenses_data = cursor.fetchall()  

            print(f"\nExpenses greater than {amount}:")
            for row in expenses_data:
                print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error with DB! ", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        more = False
        income = False
        pressEnter = input('\nPress ENTER to return at main menu')
        clearConsole(), mainMenuUser(nickname)
    elif more and all:
        try:
            connection = psycopg2.connect(
                dbname='-',    
                user='postgres',  
                password='-',  
                host='localhost',          
                port='5432'                
            )
        
            cursor = connection.cursor()

            expenses_query = """
            SELECT expensesofuser_summ, expensesofuser_dateExpenses, expensesofuser_description
            FROM ExpensesOfUser
            WHERE expensesofuser_summ > %s AND user_nickname = %s;
            """
            cursor.execute(expenses_query, (amount, nickname))
            expenses_data = cursor.fetchall() 

            income_query = """
            SELECT incomeofuser_summ, incomeofuser_dateIncome, incomeofuser_description
            FROM IncomeOfUser
            WHERE incomeofuser_summ > %s;
            """
            cursor.execute(income_query, (amount,))
            income_data = cursor.fetchall()

            print(f"\nExpenses:")
            for row in expenses_data:
                print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

            print(f"\nIncome:")
            for row in income_data:
                print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error with DB! ", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        more = False
        all = False
        pressEnter = input('\nPress ENTER to return at main menu')
        clearConsole(), mainMenuUser(nickname)
    #
    elif less and expenses:
        try:
            connection = psycopg2.connect(
                dbname='-',    
                user='postgres',  
                password='-',  
                host='localhost',          
                port='5432'                
            )

            cursor = connection.cursor()

            expenses_query = """
                SELECT expensesofuser_summ, expensesofuser_dateExpenses, expensesofuser_description
                FROM ExpensesOfUser
                WHERE expensesofuser_summ < %s AND user_nickname = %s;
            """

            cursor.execute(expenses_query, (amount, nickname))
            expenses_data = cursor.fetchall()  

            print(f"\nExpenses smaller than {amount}:")
            for row in expenses_data:
                print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error with DB! ", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        less = False
        expenses = False
        pressEnter = input('\nPress ENTER to return at main menu')
        clearConsole(), mainMenuUser(nickname)
    elif less and income:
        try:
            connection = psycopg2.connect(
                dbname='-',    
                user='postgres',  
                password='-',  
                host='localhost',          
                port='5432'                
            )

            cursor = connection.cursor()

            expenses_query = """
                SELECT incomeofuser_summ, incomeofuser_dateincome, incomeofuser_description
                FROM IncomeOfUser
                WHERE incomeofuser_summ < %s AND user_nickname = %s;
            """

            cursor.execute(expenses_query, (amount, nickname))
            expenses_data = cursor.fetchall()  

            print(f"\nExpenses smaller than {amount}:")
            for row in expenses_data:
                print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error with DB! ", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        less = False
        income = False
        pressEnter = input('\nPress ENTER to return at main menu')
        clearConsole(), mainMenuUser(nickname)
    elif less and all:
        try:
            connection = psycopg2.connect(
                dbname='-',    
                user='postgres',  
                password='-',  
                host='localhost',          
                port='5432'                
            )
        
            cursor = connection.cursor()

            expenses_query = """
            SELECT expensesofuser_summ, expensesofuser_dateExpenses, expensesofuser_description
            FROM ExpensesOfUser
            WHERE expensesofuser_summ < %s AND user_nickname = %s;
            """
            cursor.execute(expenses_query, (amount, nickname))
            expenses_data = cursor.fetchall() 

            income_query = """
            SELECT incomeofuser_summ, incomeofuser_dateIncome, incomeofuser_description
            FROM IncomeOfUser
            WHERE incomeofuser_summ < %s;
            """
            cursor.execute(income_query, (amount,))
            income_data = cursor.fetchall()

            print(f"\nExpenses:")
            for row in expenses_data:
                print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

            print(f"\nIncome:")
            for row in income_data:
                print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error with DB! ", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        less = False
        all = False
        pressEnter = input('\nPress ENTER to return at main menu')
        clearConsole(), mainMenuUser(nickname)
    #
    elif equal and expenses:
        try:
            connection = psycopg2.connect(
                dbname='-',    
                user='postgres',  
                password='-',  
                host='localhost',          
                port='5432'                
            )

            cursor = connection.cursor()

            expenses_query = """
                SELECT expensesofuser_summ, expensesofuser_dateExpenses, expensesofuser_description
                FROM ExpensesOfUser
                WHERE expensesofuser_summ = %s AND user_nickname = %s;
            """

            cursor.execute(expenses_query, (amount, nickname))
            expenses_data = cursor.fetchall()  

            print(f"\nExpenses greater than {amount}:")
            for row in expenses_data:
                print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error with DB! ", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        equal = False
        expenses = False
        pressEnter = input('\nPress ENTER to return at main menu')
        clearConsole(), mainMenuUser(nickname)
    elif equal and income:
        try:
            connection = psycopg2.connect(
                dbname='-',    
                user='postgres',  
                password='-',  
                host='localhost',          
                port='5432'                
            )

            cursor = connection.cursor()

            expenses_query = """
                SELECT incomeofuser_summ, incomeofuser_dateincome, incomeofuser_description
                FROM IncomeOfUser
                WHERE incomeofuser_summ = %s AND user_nickname = %s;
            """

            cursor.execute(expenses_query, (amount, nickname))
            expenses_data = cursor.fetchall()  

            print(f"\nExpenses greater than {amount}:")
            for row in expenses_data:
                print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error with DB! ", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        equal = False
        income = False
        pressEnter = input('\nPress ENTER to return at main menu')
        clearConsole(), mainMenuUser(nickname)
    elif equal and all:
        try:
            connection = psycopg2.connect(
                dbname='-',    
                user='postgres',  
                password='-',  
                host='localhost',          
                port='5432'                
            )
        
            cursor = connection.cursor()

            expenses_query = """
            SELECT expensesofuser_summ, expensesofuser_dateExpenses, expensesofuser_description
            FROM ExpensesOfUser
            WHERE expensesofuser_summ = %s AND user_nickname = %s;
            """
            cursor.execute(expenses_query, (amount, nickname))
            expenses_data = cursor.fetchall() 

            income_query = """
            SELECT incomeofuser_summ, incomeofuser_dateIncome, incomeofuser_description
            FROM IncomeOfUser
            WHERE incomeofuser_summ = %s;
            """
            cursor.execute(income_query, (amount,))
            income_data = cursor.fetchall()

            print(f"\nExpenses:")
            for row in expenses_data:
                print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

            print(f"\nIncome:")
            for row in income_data:
                print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

        except (Exception, psycopg2.DatabaseError) as error:
            print("Error with DB! ", error)
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()
        equal = False
        all = False
        pressEnter = input('\nPress ENTER to return at main menu')
        clearConsole(), mainMenuUser(nickname)
    #
    else:
        print('Incorrect input! Try again!'), t.sleep(4), clearConsole(), outputSelectByAmount(nickname)
def outputSelectByDate(nickname):
    date = input("Enter the date of expenses in year-month-day format (YYYY-MM-DD): ")
    is_valid, parsed_date = check_date(date)
    if is_valid:
        expenses = False
        income = False
        all = False
        print('You want to see expenses - enter 1, income - enter 2, all - enter 3')
        choiseOperation = input('Your choise: ')
        if choiseOperation == '1':
            expenses = True
        elif choiseOperation == '2':
            income = True
        elif choiseOperation == '3':
            all = True
        else:
            print('Incorrect input! Try again!'), t.sleep(4), clearConsole(), outputSelectByDate(nickname)

        ###
        if expenses:
            try:
                connection = psycopg2.connect(
                    dbname='-',    
                    user='postgres',  
                    password='-',  
                    host='localhost',          
                    port='5432'                
                )

                cursor = connection.cursor()

                expenses_query = """
                SELECT expensesofuser_summ, expensesofuser_dateExpenses, expensesofuser_description
                FROM ExpensesOfUser
                WHERE expensesofuser_dateExpenses = %s AND user_nickname = %s;
                """

                cursor.execute(expenses_query, (date, nickname))
                expenses_data = cursor.fetchall()  

                print(f"\nExpenses at {date}:")
                for row in expenses_data:
                    print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error with DB! ", error)
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
            expenses = False
            pressEnter = input('\nPress ENTER to return at main menu')
            clearConsole(), mainMenuUser(nickname)
        elif income:
            try:
                connection = psycopg2.connect(
                    dbname='-',    
                    user='postgres',  
                    password='-',  
                    host='localhost',          
                    port='5432'                
                )

                cursor = connection.cursor()
                
                expenses_query = """
                SELECT incomeofuser_summ, incomeofuser_dateincome, incomeofuser_description
                FROM incomeofuser
                WHERE incomeofuser_dateincome = %s AND user_nickname = %s;
                """

                cursor.execute(expenses_query, (date, nickname))
                expenses_data = cursor.fetchall()  

                print(f"\nExpenses at {date}:")
                for row in expenses_data:
                    print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error with DB! ", error)
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
            income = False
            pressEnter = input('\nPress ENTER to return at main menu')
            clearConsole(), mainMenuUser(nickname)
        elif all:
            try:
                connection = psycopg2.connect(
                    dbname='-',    
                    user='postgres',  
                    password='-',  
                    host='localhost',          
                    port='5432'                
                )
        
                cursor = connection.cursor()

                expenses_query = """
                SELECT expensesofuser_summ, expensesofuser_dateExpenses, expensesofuser_description
                FROM ExpensesOfUser
                WHERE expensesofuser_dateExpenses = %s AND user_nickname = %s;
                """
                cursor.execute(expenses_query, (date, nickname))
                expenses_data = cursor.fetchall() 

                income_query = """
                SELECT incomeofuser_summ, incomeofuser_dateIncome, incomeofuser_description
                FROM IncomeOfUser
                WHERE incomeofuser_dateIncome = %s;
                """
                cursor.execute(income_query, (date,))
                income_data = cursor.fetchall()

                print(f"\nExpenses:")
                for row in expenses_data:
                    print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

                print(f"\nIncome:")
                for row in income_data:
                    print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

            except (Exception, psycopg2.DatabaseError) as error:
                print("Error with DB! ", error)
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
            all = False
            pressEnter = input('\nPress ENTER to return at main menu')
            clearConsole(), mainMenuUser(nickname)
        else:
            print('App error! Try again!'), t.sleep(4), clearConsole(), outputSelectByDate(nickname)
    else:
        print("Inputed date isn't correct."), t.sleep(4), clearConsole(), enterExpenses(nickname)
def outputSelectByDescription(nickname):
    description = input('Input description of transaction: ')
    if len(description) < 1000:
        expenses = False
        income = False
        all = False
        print('You want to see expenses - enter 1, income - enter 2, all - enter 3')
        choiseOperation = input('Your choise: ')
        if choiseOperation == '1':
            expenses = True
        elif choiseOperation == '2':
            income = True
        elif choiseOperation == '3':
            all = True
        else:
            print('Incorrect input! Try again!'), t.sleep(4), clearConsole(), outputSelectByDescription(nickname)

        if expenses:
            try:
                connection = psycopg2.connect(
                    dbname='-',    
                    user='postgres',  
                   password='-',  
                    host='localhost',          
                    port='5432'                
                )

                cur = connection.cursor()

                query = """
                SELECT expensesofuser_summ, expensesofuser_dateExpenses, expensesofuser_description
                FROM ExpensesOfUser
                WHERE expensesofuser_description LIKE %s AND user_nickname = %s;
                """

                descriptionReady = '%'+description+'%'
                cur.execute(query, (descriptionReady, nickname))
                expenses_data = cur.fetchall()  
                print(f"\Description with '{description}':")
                for row in expenses_data:
                    print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error with DB! ", error)
            finally:
                cur.close()
                connection.close()
            expenses = False
            pressEnter = input('\nPress ENTER to return at main menu')
            clearConsole(), mainMenuUser(nickname)
        elif income:
            try:
                connection = psycopg2.connect(
                    dbname='-',    
                    user='postgres',  
                   password='-',  
                    host='localhost',          
                    port='5432'                
                )

                cur = connection.cursor()

                query = """
                SELECT incomeofuser_summ, incomeofuser_dateExpenses, incomeofuser_description
                FROM incomeofuser
                WHERE incomeofuser_description LIKE %s AND user_nickname = %s;
                """

                descriptionReady = '%'+description+'%'
                cur.execute(query, (descriptionReady, nickname))
                expenses_data = cur.fetchall()  
                print(f"\Description with '{description}':")
                for row in expenses_data:
                    print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")
            except (Exception, psycopg2.DatabaseError) as error:
                print("Error with DB! ", error)
            finally:
                cur.close()
                connection.close()
            income = False
            pressEnter = input('\nPress ENTER to return at main menu')
            clearConsole(), mainMenuUser(nickname)
        elif all:
            try:
                connection = psycopg2.connect(
                    dbname='-',    
                    user='postgres',  
                   password='-',  
                    host='localhost',          
                    port='5432'                
                )

                cur = connection.cursor()
                descriptionReady = '%'+description+'%'

                expenses_query = """
                SELECT expensesofuser_summ, expensesofuser_dateExpenses, expensesofuser_description
                FROM ExpensesOfUser
                WHERE expensesofuser_description LIKE %s AND user_nickname = %s;
                """
                
                cur.execute(expenses_query, (descriptionReady, nickname))
                expenses_data = cur.fetchall() 

                incomeQuery = """
                SELECT incomeofuser_summ, incomeofuser_dateIncome, incomeofuser_description
                FROM incomeofuser
                WHERE incomeofuser_description LIKE %s AND user_nickname = %s;
                """

                cur.execute(incomeQuery, (descriptionReady, nickname))
                income_data = cur.fetchall()  


                print(f"\nExpenses, description with {description}:")
                for row in expenses_data:
                    print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

                print(f"\nIncome, description with {description}:")
                for row in income_data:
                    print(f"Summ: {row[0]}, Date: {row[1]}, Description: {row[2]}")

            except (Exception, psycopg2.DatabaseError) as error:
                print("Error with DB! ", error)
            finally:
                cur.close()
                connection.close()
            all = False
            pressEnter = input('\nPress ENTER to return at main menu')
            clearConsole(), mainMenuUser(nickname)
        else:
            print('Error app! Try again!'), t.sleep(4), clearConsole(), outputSelectByDescription(nickname)
    else:
        print('Character limit exceeded! Try again!'), t.sleep(4), clearConsole(), enterExpenses(nickname) 

def visualizationIncomes(nickname):
    connection = psycopg2.connect(
        dbname='-',    
        user='postgres',  
        password='-',  
        host='localhost',          
        port='5432'                
    )

    query = f"SELECT incomeofuser_summ FROM incomeofuser WHERE user_nickname = '{nickname}';"
    df = pd.read_sql_query(query, connection)
    connection.close()

    plt.plot(df['incomeofuser_summ'], marker='o')
    plt.title(f'Income of {nickname}')
    plt.xlabel('Record Number')
    plt.ylabel('Income Summ')
    plt.grid()
    plt.show()
def visualizationExpenses(nickname):
    connection = psycopg2.connect(
        dbname='-',
        user='postgres',
        password='-',
        host='localhost',
        port='5432'
    )

    query = f"SELECT expensesofuser_summ FROM expensesofuser WHERE user_nickname = '{nickname}';"
    df = pd.read_sql_query(query, connection)
    connection.close()

    plt.plot(df['expensesofuser_summ'], marker='o')
    plt.title(f'Expenses of {nickname}')
    plt.xlabel('Record Number')
    plt.ylabel('Expense Summ')
    plt.grid()
    plt.show()
