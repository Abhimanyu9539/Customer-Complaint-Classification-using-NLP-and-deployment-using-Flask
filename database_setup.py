'''
Project : Data Talent Complaint Processing
Author: Abhimanyu Dasarwar
Date Created : 07/07/2020

Purpose:
    1.Setup the database
    2.Create db file
    3.Create table in the db 
'''


import sqlite3

# The database will be created in the location where 'py' file is saved
db_name = 'complaints_data.db'

# Connect with the data base
conn = sqlite3.connect(db_name) 

# Create cursor object 
c = conn.cursor()

# Define the schema of table to be created.
sql_table = """ 
            CREATE TABLE IF NOT EXISTS complaints(
            firstname text,
            lastname text,
            invoice_number int,
            invoice_date text,
            product_name text,
            complaint_nature text,
            department text,
            reference_number text,
            status text
            
            )
            """

# Create SQL Table
def create_complaints_table(conn, sql_table):    
    c = conn.cursor()
    c.execute(sql_table)

# Call the create_sql_table method
create_complaints_table(conn,sql_table)

# commit changes to database
conn.commit()


'''
End Result:
    This script creates database, also it defines the table schema of the table.
    As well as it creats the table in the database.
'''
