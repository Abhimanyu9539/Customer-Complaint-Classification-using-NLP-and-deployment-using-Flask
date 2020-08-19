# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:11:09 2020

@author: ACER

Purporse:
    1.To train a ML Model which will classify the product departments.
"""

### Customer Classification using Complaints Database

# Creating a ML Model to classify the customers in to different Departments of Complaints.

## Import required libraries
import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import SGDClassifier
from sklearn import svm

### Step 1: Import Database into a Dataframe
complaints = pd.read_csv('Consumer_Complaints.csv')
complaints.head()

## Database summary
complaints.shape

## Checking null values in df
complaints.isnull().sum()

## columns in df
complaints.columns

## For the Model building and classification, we will be looking at `"Product" and "Consumer Complaint Narrative"` columns only.
complaints = complaints[['Product','Issue', 'Consumer complaint narrative']]
complaints.head()
complaints.isnull().sum()
## dropping null values from the df
complaints.dropna(axis=0, inplace=True)

'''
There are different type of Categories those can be merged together so that Number of Complaint Nature can be reduced.

For eg: "Credit card or prepaid card" and "Prepaid Card" can be merged together.
'''

## Merging the related categories together
complaints[complaints['Product']== 'Virtual currency'] = 'Money Transfer'
complaints[complaints['Product']== 'Money transfer, virtual currency, or money service'] = 'Money Transfer'
complaints[complaints['Product']== 'Money transfers'] = 'Money Transfer'

## Credit card and Virtual Card Categories
complaints[complaints['Product']== 'Prepaid card'] = 'Credit card or prepaid card'
complaints[complaints['Product']== 'Credit card'] = 'Credit card or prepaid card'
complaints[complaints['Product']== 'Credit reporting'] = 'Credit reporting, credit repair services, or other personal consumer reports'

## Vehicle loan or lease, Consumer Loan
complaints[complaints['Product']== 'Vehicle loan or lease'] = 'Consumer Loan, Vehicle Loan or Lease'
complaints[complaints['Product']== 'Consumer Loan'] = 'Consumer Loan, Vehicle Loan or Lease'

## Payday Loan, Title Loan or Personal Loan
complaints[complaints['Product']== 'Payday loan'] = 'Payday Loan, Title Loan, Personal Loan or Student Loan'
complaints[complaints['Product']== 'Student loan'] = 'Payday Loan, Title Loan, Personal Loan or Student Loan'
complaints[complaints['Product']== 'Payday loan, title loan, or personal loan'] = 'Payday Loan, Title Loan, Personal Loan or Student Loan'

complaints['Product'].value_counts()

## Checking null values in df
complaints.isnull().sum()

y = complaints['Product']
X = complaints['Consumer complaint narrative']

X_train, X_test, y_train, y_test =train_test_split(X,y,train_size=0.7,test_size=0.3, random_state=42) 

# Creating a pipeline
pipeline = Pipeline(steps= [('tfidf', TfidfVectorizer()),
                           # ('NaiveBayes', MultinomialNB()),
                           ('SGD', SGDClassifier())])
                           #('RF', RandomForestClassifier())])
                           
pipeline.fit(X_train,y_train)
y_train_pred = pipeline.predict(X_train)

## Accuracy of the model on train data
np.mean(y_train_pred == y_train)

## Predict the values for test data
y_pred = pipeline.predict(X_test)

## Accuracy of the model on test data
np.mean(y_pred == y_test)

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

print(accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))

text = ["I want to a Loan to buy laptop"]
pipeline.predict(text)

from joblib import dump
dump(pipeline , filename="complaint_classification.joblib")

























