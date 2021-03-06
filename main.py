# -*- coding: utf-8 -*-
import uvicorn
from fastapi import FastAPI

import database
import datamodels
import pandas as pd

from datetime import date

import nest_asyncio


nest_asyncio.apply()

app = FastAPI(title= 'goCloud Test Project', version = '1.0', description = "Enjoy this fully functional bank system API!!!")

@app.get('/')
def read_home():
    return {'message': 'Test Project API live!'}

@app.post('/CreateCustomer/')
# Endpoint takes in an object of the type new customer
# Following that, each part is added to its column
def create_user(data: datamodels.new_customer):
    
    data = data.dict()
    
    FirstName = data['FirstName']
    LastName = data['LastName']
    DateOfBirth = data['DateOfBirth']
    StreetName = data['StreetName']
    HouseNumber = data['HouseNumber']
    PostCode = data['PostCode']
    City = data['City']
    Country = data['Country']
    
    conn = database.connectdb()
    cursor = conn.cursor()
    cursor.execute(""" INSERT INTO customertable(FirstName, LastName, DateOfBirth, StreetName, HouseNumber, PostCode, City, Country) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", (FirstName, LastName, DateOfBirth, StreetName, HouseNumber, PostCode,
                   City, Country))
    conn.commit()
    cursor.close()
    return {'message': 'New customer created successfully'}

@app.post('/GetCustomersByLastname/')
def get_customers_by_last_name(data: datamodels.lastname_sort):
    ## The incoming data model is transformed into a dictionary
    data = data.dict()
    
    LastName = data['LastName'][0]
    Sort = str(data['Sort'][0]).lower()
    
    conn = database.connectdb()
    cursor = conn.cursor()
    
    cursor.execute(""" SELECT FirstName, LastName, StreetName, HouseNumber, PostCode, City, Country FROM customertable 
                 WHERE LastName = '%s' """,(LastName))
    ## The found data is saved into a list and sorted according to the value of Sort
    customers = cursor.fetchall()
    customers = list(customers)
    
    if Sort == 'desc':
        customers = sorted(customers, key = lambda x: x[1], reverse = True)
    else:
        customers = sorted(customers, key = lambda x: x[1])
           
    return customers
  
@app.post('/CreateNewAccount/')
def create_new_account(data: datamodels.new_account):
    
    #In order to create a new account, send CustomerId. A new account will be allocated.
    
    data = data.dict()
    
    CustomerId = data['CustomerId']
    
    conn = database.connectdb()
    cursor = conn.cursor()
    
    cursor.execute("""INSERT INTO accounttable(CustomerId) VALUES (%s)""" % (CustomerId))
    
    conn.commit()
    
    cursor.close()
    return {'message': 'New account created successfully'}
@app.post('/CreateNewCredit/')
def create_new_credit(data: datamodels.new_credit):
    
    ##Information about credit recipient is received and trasformed into a dictionary
    data = data.dict()
    
    
    AccountId = data['AccountId']
    CustomerId = data['CustomerId']
    TotalCreditAmount = data['TotalCreditAmount']
    CreditIssueDate = data['CreditIssueDate']
    ToBePaidBefore = data['ToBePaidBefore']
    BankId = 1
    conn = database.connectdb()
    cursor = conn.cursor()
    
    SQL_Query = pd.read_sql_query(""" SELECT CurrentBalance FROM accounttable WHERE Id = '' """ % (BankId), conn)
    BankBalance = pd.DataFrame(SQL_Query, columns = ['CurrentBalance'])
    
    SQL_Query = pd.read_sql_query(""" SELECT CurrentBalance FROM accounttable WHERE Id = '%s' """ % (AccountId), conn)
    df = pd.DataFrame(SQL_Query, columns = ['CurrentBalance'])
    
    ## Check if bank has sufficient funds, if yes, the credit will be issued
    
    if float(BankBalance['CurrentBalance'][0]) >= float(TotalCreditAmount):
        ## Credit amount added to credit recipient and subtracted from bank account
        NewAccountBalance = float(df['CurrentBalance'][0]) + float(TotalCreditAmount)
        NewBankBalance = float(BankBalance['CurrentBalance'][0]) - float(TotalCreditAmount)
        
        cursor.execute (""" UPDATE accounttable SET CurrentBalance = %s WHERE Id = %s""", (NewAccountBalance, AccountId))
        
        cursor.execute (""" UPDATE accounttable SET CurrentBalance = %s WHERE Id = %s""", (NewBankBalance, BankId))
        cursor.execute(""" INSERT INTO credittable(AccountId, CustomerId, TotalCreditAmount, CreditIssueDate, ToBePaidBefore, RemainingAmountToBePaid) 
                       VALUES (%s, %s, %s, %s, %s, 5S)""", (AccountId, CustomerId, TotalCreditAmount, CreditIssueDate, ToBePaidBefore, TotalCreditAmount))    
    
        conn.commit()
    
        return {'message': 'New Credit Successfully Created'}
    else:
        return {'message': 'New Credit Cannot Be Issued At The Moment'}

@app.post('/Transfer/')
def transfer_money(data: datamodels.transfer_money):
    
    ##Information about transfer sender and recipient is received and trasformed into a dictionary
    
    data = data.dict()
    
    SendingAccountId = data['SendingAccountId']
    ReceivingAccountId = data['ReceivingAccountId']
    Amount = float(data['Amount'])
    
    conn = database.connectdb()
    cursor = conn.cursor()
    
    SQL_Query = pd.read_sql_query(""" SELECT CurrentBalance FROM accounttable WHERE Id = '%s' """ % (SendingAccountId), conn)
    SendingAccBalance = pd.DataFrame(SQL_Query, columns = ['CurrentBalance'])
    
    SQL_Query = pd.read_sql_query(""" SELECT CurrentBalance FROM accounttable WHERE Id = '%s' """ % (ReceivingAccountId), conn)
    ReceivingAccBalance = pd.DataFrame(SQL_Query, columns = ['CurrentBalance'])
    
    SendingAccBalance = float(SendingAccBalance['CurrentBalance'][0])
    ReceivingAccBalance = float(ReceivingAccBalance['CurrentBalance'][0])
    
    ## Check if the sending and receiving accounts are the same, if not continue

    if SendingAccountId != ReceivingAccountId:
        
        ## Check if the sender has enough money
        if  SendingAccBalance > Amount:
            
            ## Subtract the amount from sender and add to recipient
            NewSendingAccBalance = SendingAccBalance - Amount
            NewReceivingAccBalance = ReceivingAccBalance + Amount
            
            cursor.execute (""" UPDATE accounttable SET CurrentBalance = %s WHERE Id = %s""", (NewSendingAccBalance, SendingAccountId))
            
            
            cursor.execute (""" UPDATE accounttable SET CurrentBalance = %s WHERE Id = %s""", (NewReceivingAccBalance, ReceivingAccountId))
            
            
            cursor.execute(""" INSERT INTO postingtable(SendingAccountId, ReceivingAccountId, Amount) 
                   VALUES (%s, %s, %s)""", (SendingAccountId, ReceivingAccountId, Amount))
            
            
            conn.commit()
            
            return {'message': 'Transfer Successful'}
        
        else:
            return {'message': 'Insufficient Funds'}
        
    else:
        return {'message': 'Receiving Account Has To Be Different From The Sending Account'}
        
@app.get('/GetAllAccounts/')
def get_all_accounts_of_customer(CustomerId: int):
    
    conn = database.connectdb()
    
    SQL_Query = pd.read_sql_query(""" SELECT Id, CurrentBalance FROM accounttable WHERE CustomerId = '%s' """ % (CustomerId), conn)
    CustomerAccounts = pd.DataFrame(SQL_Query, columns = ['Id','CurrentBalance'])
    
    CustomerAccounts = CustomerAccounts.values.tolist()
    
    return CustomerAccounts

@app.get('/GetAllCredits/')
def get_all_credits_of_customer(CustomerId: int):
    
    conn = database.connectdb()   
    
    SQL_Query = pd.read_sql_query(""" SELECT TotalCreditAmount, RemainingAmountToBePaid, CreditIssueDate, ToBePaidBefore FROM credittable WHERE CustomerId = '%s' """ % (CustomerId), conn)
    CustomerCredits = pd.DataFrame(SQL_Query, columns = ['TotalCreditAmount','RemainingAmountToBePaid', 'CreditIssueDate', 'ToBePaidBefore'])
    
    CustomerCredits = CustomerCredits.values.tolist()
    
    return CustomerCredits

@app.get('/GetAllBookings/')  
def get_all_bookings(BookingDate: date):
    
    conn = database.connectdb() 
    SQL_Query = pd.read_sql_query(""" SELECT SendingAccountId, ReceivingAccountId, Amount, TransferDateTime FROM postingtable WHERE BookingDate = '%s' """ % (BookingDate), conn)
    Bookings = pd.DataFrame(SQL_Query, columns = ['SendingAccountId','ReceivingAccountId', 'Amount', 'TransferDateTime'])
    
    return Bookings.values.tolist()
@app.get('/GetAllPostings/') 
def get_all_postings(data: datamodels.all_postings_individual):
    
    data = data.dict()
    
    SendingAccountId = data['AccountId']
    SendingCustomerFirstName = data['SendingCustomerFirstName'].str()
    SendingCustomerLastName = data['SendingCustomerLastName'].str()
    ReceivingAccountId = data['ReceivingAccountId']
    Sort = str(data['Sort'][0]).lower()
    Skip = data['Skip']
    Limit = data['Limit']
    
    conn = database.connectdb() 
    
    SQL_Query = pd.read_sql_query(""" SELECT customertable.FirstName, customertatble.LastName, postingtable.Id, postingtable.SendingAccountId, postingtable.ReceivingAccountId, postingtable.Amount, TransferDateTime 
                                  FROM postingtable 
                                  JOIN accounttable ON postingtable.SendingAccountId = accounttable.Id
                                  JOIN customertable ON accounttable.CustomerId = customertable.Id
                                  WHERE postingtable.SendingAccountId = %s AND postingtable.ReceivingAccountId = %s   
                                  ORDER BY customertable.FirstName OFFSET""" + Skip + """ ROWS FETCH NEXT """ + Limit + """ ROWS ONLY """, 
                                  (SendingAccountId, ReceivingAccountId), conn)
    
    Postings = pd.DataFrame(SQL_Query, columns = ['FirstName', 'LastName''Id','SendingAccountId', 'ReceivingAccountId', 'Amount', 'TransferDateTime'])
    Postings[Postings['FirstName'].str.match(SendingCustomerFirstName)]
    
    Postings[Postings['FirstName'].str.match(SendingCustomerLastName)]
    
    if Sort == 'desc':
        
        Postings = Postings.sort('FirstName', ascending = False)
    
    return Postings
@app.post('/PayoffCredit/')
def payoff_credit(data: datamodels.payoff_credit):
    
    
    data = data.dict()   
    
    SendingAccountId = data['AccountId']
    CreditId = data['CreditId']
    Amount = float(data['Amount'])
    
    BankId = 1
    
    conn = database.connectdb()
    cursor = conn.cursor()
    
    SQL_Query = pd.read_sql_query(""" SELECT CurrentBalance FROM accounttable WHERE Id = '%s' """ % (SendingAccountId), conn)
    SendingAccBalance = pd.DataFrame(SQL_Query, columns = ['CurrentBalance'])
    
    SQL_Query = pd.read_sql_query(""" SELECT RemainingAmountToBePaid FROM credittable WHERE Id = '%s' """ % (CreditId), conn)
    RemainingAmountToBePaid = pd.DataFrame(SQL_Query, columns = ['RemainingAmountToBePaid'])
    
    SQL_Query = pd.read_sql_query(""" SELECT Rating FROM credittable WHERE Id = '%s' """ % (CreditId), conn)
    Rating = pd.DataFrame(SQL_Query, columns = ['Rating'])
    Rating = float(Rating['Rating'][0])
    
    SQL_Query = pd.read_sql_query(""" SELECT CurrentBalance FROM accounttable WHERE Id = '' """ % (BankId), conn)
    BankBalance = pd.DataFrame(SQL_Query, columns = ['CurrentBalance'])
    
    SQL_Query = pd.read_sql_query(""" SELECT CustomerId FROM credittable WHERE Id = '%s' """ % (CreditId), conn)
    CreditCustomerId = pd.DataFrame(SQL_Query, columns = ['CustomerId'])
    CreditCustomerId = float(CreditCustomerId['CreditCustomerId'][0])
    
    
    
    message = 'You have successfully paid a part of your credit'
    
    ## Check if sender has enough money
    
    if  float(SendingAccBalance['CurrentBalance'][0]) > Amount:
        
        ## Check if the credit has been paid or not
        
        if float(RemainingAmountToBePaid['RemainingAmountToBePaid'][0]) > 0:
        
            ## Subtract the amount from account balance and recalculate remaining part to be paid
            NewSendingAccBalance = float(SendingAccBalance['CurrentBalance'][0]) - Amount
            NewRemainingAmountToBePaid = float(RemainingAmountToBePaid['RemainingAmountToBePaid'][0]) - Amount
            
            
            ## Add the money to the bank account
            
            NewBankBalance = float(BankBalance['CurrentBalance'][0]) + Amount
            
            ## Check if the remaining amount is zero or below zero. If yes, it means that the has been paid,
            ## the credit gets marked as paid and the customer receives an increased rating. If the customer
            ## paid more money than he was supposed to, the money gets reimbursed.
            
            if NewRemainingAmountToBePaid <= 0:
                
                NewRemainingAmountToBePaid = 0
                message = 'Congratulations, You have completely paid off your credit'
                
                if Rating != 1:
                    Rating = Rating - 1
            
            cursor.execute (""" UPDATE accounttable SET CurrentBalance = %s WHERE Id = %s""", (NewSendingAccBalance, SendingAccountId))
            
            cursor.execute (""" UPDATE credittable SET Rating = %s WHERE Id = %s""", (Rating, CreditCustomerId))
            
            cursor.execute (""" UPDATE credittable SET RemainingAmountToBePaid = %s, IsPaidOff = TRUE  WHERE Id = %s""", (NewRemainingAmountToBePaid, CreditId))
            
            cursor.execute (""" UPDATEaccounttable SET CurrentBalance = %S WHERE Id = %s""", (NewBankBalance, BankId))
                      
            
            conn.commit()
            
            
            return {'message': message}
        else:
            return {'message': 'This Credit Has Already Been Paid Off'}
    else:
            return {'message': 'Insufficient Funds'}
        
@app.get('/GetCustomerBalance/')
def get_customer_balance(CustomerId: int):
    
    conn = database.connectdb()
    
    SQL_Query = pd.read_sql_query(""" SELECT CurrentBalance FROM accounttable WHERE CustomerId = '%s' """ % (CustomerId), conn)
    CurrentBalances = pd.DataFrame(SQL_Query, columns = ['CurrentBalance'])
    
    Total = CurrentBalances['CurrentBalance'].sum()
    
    return {'Customer Total Balance': float(Total)}
    
@app.get('/GetExceededCredits/')
def get_exceeded_credits():
    
    conn = database.connectdb()
    
    SQL_Query = pd.read_sql_query(""" SELECT credittable.TotalCreditAmount, credittable.RemainingAmountToBePaid, customertable.FirstName, customertable.LastName 
                                  FROM accounttable 
                                  JOIN customertable ON credittable.CustomerId = customertable.Id
                                  WHERE credittable.IsPaidOff =False AND credittable.IsOverdue = TRUE""" , conn)
                                  
    OverdueCredits = pd.DataFrame(SQL_Query, columns = ['TotalCreditAmmount', 'RemainingAmountToBePaid','FirstName', 'LastName'])
    
    OverdueCredits = OverdueCredits.values.tolist()
    
    return OverdueCredits
    
@app.get('/GetAllCustomersGroupedByRating/')
def get_all_customers_grouped_by_rating():    
    conn = database.connectdb()
    
    SQL_Query = pd.read_sql_query(""" SELECT Id, FirstName, LastName, Rating
                                  FROM customertable 
                                  GROUP BY Rating""" , conn)
    CustomersGroupedByRating = pd.DataFrame(SQL_Query, columns = ['Id', 'FirstName','LastName', 'Rating'])
    
    CustomersGroupedByRating = CustomersGroupedByRating.values.tolist()
    
    return CustomersGroupedByRating

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8007)