# -*- coding: utf-8 -*-
"""
Created on Sun Jul  5 13:50:17 2020
Project : Data Talent Complaint Processing
Author: Abhimanyu Dasarwar

Purpose:
    1.Online Reception of complaints
    2.Establishing and storing application data in Database.
    3.Rendering HTML and accepting user input.
"""

'''Import Required libraries'''
from flask import Flask, render_template, request
import sqlite3
import logging

#initialize logging
LOG_FILE_NAME = 'DataTalentAppLog.txt'
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=LOG_FILE_NAME,
                    filemode='w')
    

'''Load the ML Model for classifying the complaint'''
from joblib import dump, load
# load the saved model
complaint_app = load('complaint_classification.joblib')


'''Establish connection with database'''
def db_connect():
    # establsih the connection
    db_name = 'complaints_data.db'
    db_con = sqlite3.connect(db_name)
    logging.info('Connected to '+db_name)
    return db_con

conn = db_connect()



''' Write the data into table '''
def write_data_into_db(complaints_data):

    # establsih the connection
    conn = db_connect()

    # create a cursor
    cur = conn.cursor()
    try:
        # insert data into complaints table in db
        sql = 'insert into complaints(' \
              'firstname,' \
              'lastname,' \
              'invoice_number,' \
              'invoice_date, ' \
              'product_name, ' \
              'complaint_nature,'\
              'department,'\
              'reference_number,'\
              'status) values(?,?,?,?,?,?,?,?,?)'
              
      
        # verifying the sql statement for debug
        print(sql)
        
        # Creating unique reference number for customer
        # it is a combination of last name, invoice number and product name
        refno = complaints_data[1][:4] + complaints_data[4][:3]+ complaints_data[2][:3]
        print(refno)
        
        
        # Get the department for the complaint
        d = complaints_data[5]
        d1 = [d]
        print(d)
        dept = complaint_app.predict(d1)
        print(dept)
        complaints_data.append(dept[0])
        
        # Append reference number to complaint data
        complaints_data.append(refno)
        
        # Append "Pending" status to complaint data
        complaints_data.append("Pending")
        
        # Write data to database
        cur.execute(sql,complaints_data)
        cur.execute("commit")
        print(refno)
        
        # Close the connection
        cur.close()
        conn.close()
        logging.info("DB commit successful")
        return refno
    except:
        logging.info("DB commit unsuccessful")

''' Classify the complaint department'''
def retrieve_dept_name(complaints_data):
    dept = complaint_app.predict(complaints_data[5])
    print(dept)
    return dept

''' Retrieve complaint data from tabel'''
def retrieve_data_from_db(ref_num):
    data =[]
    conn = db_connect()
    cursor = conn.cursor()
    
    try:
        reference_number=ref_num
        cursor.execute("SELECT * from complaints WHERE reference_number = ?", [reference_number] )
        logging.info("Complaint data retrieved successfully.")    
        conn.commit()
        data = cursor.fetchall()
        return data
    except:
        logging.info("Error! Complaint data not retrieved.") 
    
    
app = Flask(__name__, template_folder="templates")

## Home Page
@app.route("/")
def index():
   return render_template("/home.html")

## Complaint registration
@app.route('/complaints.html',methods=['POST', 'GET'])

def complaint_registration():
    complaints = []
    complaint_status = ""
    if request.method == 'POST':
        try:
            logging.info("Capturing app data " + request.form['firstname'])
            complaints.append(request.form['firstname'])
            complaints.append(request.form['lasttname'])
            complaints.append(request.form['invoice_number'])
            complaints.append(request.form['invoice_date'])
            complaints.append(request.form['product_name'])
            complaints.append(request.form['Complaint_nature'])
            
            logging.info(complaints)
            
            ## Calling write_data_into_db to insert data into table
            ref_number = write_data_into_db(complaints)
            
            ## Retrieving reference id of new complaint.
            complaint_status = "Your complaint is successfully submitted with Reference Id " +str(ref_number)  + '..!'
            logging.info(complaint_status)
        except:
            complaint_status = 'Error!'
            logging.exception(complaint_status)
              
    return render_template('complaints.html', complaint_status = complaint_status)  


## Track Complaint Status
@app.route('/track_status.html', methods=['POST', 'GET'])
def  track_your_complaint_status():
    data =[]
    if request.method == "POST":
        try:
            # Accepting reference number from customer
            reference_number = request.form['ref_num_form']
            print(reference_number)
            
            ## Call retrieve_data_from_db
            data = retrieve_data_from_db(reference_number)
            logging.info(data)
            
        except:
            ref_num = 'Error!'
            logging.exception(ref_num)
        
    return render_template('track_status.html', data=data)
   

## Main Method
if __name__ == '__main__':
    app.run()


