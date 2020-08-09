# -*- coding: utf-8 -*-
import configparser
import mysql.connector as connector

config = configparser.ConfigParser()
config.read('config.ini')

host = str(config.get('MYSQLDB','host'))
password = str(config.get('MYSQLDB','password'))
database = str(config.get('MYSQLDB','database'))
user = str(config.get('MYSQLDB','user'))


## If password and username are needed, set Trusted_Connection to No and 
## use following variables:
    # User =  str(config.get('MSSQLDB','user'))
    # Password =  str(config.get('MSSQLDB','pw'))

def connectdb():
    # conn = pyodbc.connect('Driver={%s};''Server=%s;''Database=%s;''Trusted_Connection=%s' % ( Driver, Server, Database, Trusted_Connection ) )
    conn = connector.connect(   host=host,
                                         database=database,
                                         user=user,
                                         password=password)
    return conne

