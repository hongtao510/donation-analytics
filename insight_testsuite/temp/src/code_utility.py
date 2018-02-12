#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
utility functions for find_political_donors.py
'''
from datetime import datetime
from math import ceil


def valid_Zip(zipcode_str):
    '''
        Function to check if ZIP_CODE is valid, 
        should be at least 5 digits and no more than 9 digits

        Returns a boolean

        Test:
        valid_Zip("01032017") -> True
        valid_Zip("0103") -> False
    '''
    if not (zipcode_str.isdigit()):
        return False
    elif len(zipcode_str) < 5 or len(zipcode_str) > 9:
        return False
    else:
        return True


def valid_Date(date_str):
    '''
        Function to check if TRANSACTION_DT is valid, 
        should be a 8-digit str, 01032017
        first 2 represents month, 01, 
        second 2 represents day, 03,
        last 4 represents year, 2017

        Returns a boolean

        Test:
        valid_Date("01032017") -> True
        valid_Date("0103201") -> False
    '''
    if len(date_str) != 8:
        return False
    else:
        try:
            datetime.strptime(date_str, '%m%d%Y')
            return True
        except:
            return False

def valid_AMT(amt_str):
    '''
        Function to check if TRANSACTION_AMT is valid, 
        should be numeric and >0

        Returns a boolean
    '''
    if (amt_str.isdigit() and float(amt_str) > 0):
        return True
    else:
        return False



def extract_row(row_record):
    '''
        Function to parse political donors row record

        returns a tuple with two elements
            a dictionary, rslt (TRANSACTION_DT, ZIP_CODE, CMTE_ID,
                TRANSACTION_AMT, OTHER_ID)
            a binary value (to indicate whether or not to use 
                this record 0-keep, 1-drop

        if record is invalid, 
            will return an empty dictionary and ignore_record with 1
    '''
    rslt = {}                   # initialize a dictionary to hold parsed fields
    ignore_record = 0           # 0-keep, 1-drop;
    # first position-date, second-zip
    try:
        temp_l = row_record.split("|")  # split string by pip ("|")
        CMTE_ID = temp_l[0]
        NAME = temp_l[7]
        ZIP_CODE = temp_l[10]
        TRANSACTION_DT = temp_l[13]
        TRANSACTION_AMT = temp_l[14]
        OTHER_ID = temp_l[15]

        # validate CMTE_ID
        if len(CMTE_ID.strip()) > 0:
            rslt["CMTE_ID"] = CMTE_ID
        else:
            rslt["CMTE_ID"] = "_ERROR_"
            ignore_record = 1

        # validate NAME
        if len(NAME.strip()) > 0:
            rslt["NAME"] = NAME
        else:
            rslt["NAME"] = "_ERROR_"
            ignore_record = 1

        # validate TRANSACTION_DT
        if valid_Date(TRANSACTION_DT):
            rslt["TRANSACTION_DT"] = TRANSACTION_DT
        else:
            rslt["TRANSACTION_DT"] = "_ERROR_"
            ignore_record = 1

        # validate ZIP_CODE
        if valid_Zip(ZIP_CODE):
            rslt["ZIP_CODE"] = str(ZIP_CODE[0:5])
        else:
            rslt["ZIP_CODE"] = "_ERROR_"
            ignore_record = 1

        # validate OTHER_ID
        if len(OTHER_ID.strip()) == 0:
            rslt["OTHER_ID"] = ""
        else:
            rslt["OTHER_ID"] = OTHER_ID
            ignore_record = 1

        # validate TRANSACTION_AMT, has to be a numeric value and >0
        if valid_AMT(TRANSACTION_AMT):
            rslt["TRANSACTION_AMT"] = float(TRANSACTION_AMT)
        else:
            ignore_record = 1
            rslt["TRANSACTION_AMT"] = "_ERROR_"
            
    except:
        ignore_record = 1
    return rslt, ignore_record


def calculate_metric(x, pctl):
    """Function to calculate 
    1. percentile using the nearest-rank method.
    https://en.wikipedia.org/wiki/Percentile#The_nearest-rank_method
    2. count frequency
    3. calculate total

    # Returns
        three tuples
    """

    n = int(ceil(pctl / 100.0 * len(x)))
    return x[n - 1], sum(x), len(x)

def dateCompare(exist_DT, current_DT):
    '''
    Function to compare two , return true if current_DT (current record) 
    is later than exist_DT (exist)
    '''
    try:
        exist_DT_parsed = datetime.strptime(exist_DT, '%m%d%Y')
        current_DT_parsed = datetime.strptime(current_DT, '%m%d%Y')
        if exist_DT_parsed < current_DT_parsed:
            return True
        else:
            return False
    except:
        return False

def format_output(record_key, record_value, pctl):
    """Function to call calculate metrics and format output strings
    # Returns
        strings of output
    """

    record_list_t = record_key.split(', ')
    CMTE_ID_t = record_list_t[0]
    ZIP_CODE_t = record_list_t[1]
    TRANSACTION_YEAR_t = record_list_t[2]

    METRICS_t = calculate_metric(record_value, pctl)
    perctil_donation_t = str(int(round(METRICS_t[0])))
    sum_donation_t = str(int(round(METRICS_t[1])))
    n_donation_t = str(int(round(METRICS_t[2])))

    # concatenate different fields following output format
    output_str = CMTE_ID_t + "|" + ZIP_CODE_t + "|" + \
        TRANSACTION_YEAR_t + "|" + perctil_donation_t + \
        "|" + sum_donation_t + "|" + n_donation_t + "\n"

    return output_str