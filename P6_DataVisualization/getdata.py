#!/usr/bin/python
# -*-coding: utf-8-*-

"""
Using the file to minize the dataset that contains all variable,
which is used to visialize the information.
"""

# import package
import pandas as pd

# load original data
raw_data = pd.read_csv("./data/prosperLoanData.csv")

# select the features and chage the columns' name
column_name = ["BorrowerState", "ProsperRating (Alpha)", "LoanOriginalAmount",
               "LoanOriginationDate", "IncomeRange", "Occupation",
               "StatedMonthlyIncome", "TotalTrades", "LoanStatus"]

dataset = raw_data.loc[:, column_name]

dataset.colums = ["BorrowerState", "ProsperRating", "LoanOriginalAmount",
                  "LoanOriginationDate", "IncomeRange", "Occupation",
                  "StatedMonthlyIncome", "TotalTrades", "LoanStatus"]

dataset.to_csv("./data/dataset.csv")
