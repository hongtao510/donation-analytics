#!/usr/bin/env python2
# -*- coding: utf-8 -*-

'''
Main script used to process political contribution text file and generate 
an output file "repeat_donors.txt" (default name), which is a plain text file, 
with recipient ID,  zipcode, year, percentile of donations, total amount of donation, 
and total number of contributions (e.g., C00003251|45503|2018|4|1|4)

How to run this scripts:
    $ python ./src/main.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt
'''

from code_utility import *
import bisect 
import sys

def parse_file(fn_itcont, fn_pctl, fname_output):
    '''
        Function to calculate date dependent political contribution metrics for 
        each candidate. It has two parts:
            1) open input file of political contributions; read each
               line and select recipient of this contribution (CMTE_ID), 
               transaction date (TRANSACTION_DT), amount (TRANSACTION_AMT), and 
               whether contribution came from a person or an entity (OTHER_ID).
            2) once all the inputs are parsed, it calculates median contributions, 
               total transactions, and total contributions for each recipient on
               a given date. This is different from function process_zip which 
               calculates those metrics on the fly in the input file streaming
               step.
        inputs:
            fn_itcont: input file name with donation raw data
            fn_pctl: input file name with desired percentile value
            fname_output: output file name
        outputs:
            this function will generate a plain text output file (default name
            "repeat_donors.txt", separated by "|") with recipient ID, 
            zipcode, year, percentile of donations, total amount of donation, 
            and total number of contributions (e.g., C00003251|45503|2018|4|1|4)
    '''

    repeat_donors = {}          # initialize a unique ID for donors (NAME+ZIP)
    recipient_record = {}       # initialize a unique ID for recipients (CMTE_ID+ZIP+YEAR)

    try:
        writer_output = open(fname_output, 'w')

        with open(fn_pctl) as perc:
            percentile = float(perc.read())

        with open(fn_itcont, "r") as r:
            for each_line in r:
                parsed_line, ignore_record = extract_row(
                    each_line.rstrip('\n'))
                
                # if this row is valid
                if ignore_record == 0:
                    parsed_line['TRANSACTION_YEAR'] = parsed_line['TRANSACTION_DT'][-4:]
                    # create a unique ID for donors
                    parsed_line['DONOR_ID'] = parsed_line['NAME'] + ', ' + parsed_line['ZIP_CODE']
                    # a unique ID for recipients
                    parsed_line['RECIPIENT_ID'] = parsed_line['CMTE_ID'] + ", " + parsed_line['ZIP_CODE'] + ', ' + parsed_line['TRANSACTION_YEAR']
                    # print parsed_line['CMTE_ID'], parsed_line['NAME'], parsed_line['ZIP_CODE'], parsed_line['TRANSACTION_DT'], parsed_line['TRANSACTION_AMT']

                    # check each streamed record and decide if this donor is a repeated one.
                    #   1. if not, just add DONOR_ID to repeat_donors for further use (identify repeat donors)
                    #   2. otherwise, it is a repeat donor 
                    #      2.1 if data are in correct order (current row year > existing), add donation amount to recipient_record
                    #      2.2 if data are out of order, update repeat_donors value to the earlier one
                    if parsed_line['DONOR_ID'] not in repeat_donors:
                        repeat_donors[parsed_line['DONOR_ID']] = parsed_line['TRANSACTION_DT']
                    else:
                        if dateCompare(repeat_donors[parsed_line['DONOR_ID']], parsed_line['TRANSACTION_DT']):
                            if parsed_line['RECIPIENT_ID'] in recipient_record:
                                bisect.insort(recipient_record[parsed_line['RECIPIENT_ID']], parsed_line['TRANSACTION_AMT'])
                            else:
                                recipient_record[parsed_line['RECIPIENT_ID']] = [parsed_line['TRANSACTION_AMT']]
                            output_str = format_output(parsed_line['RECIPIENT_ID'], recipient_record[parsed_line['RECIPIENT_ID']], percentile)
                            writer_output.write(output_str)
                        else:
                            repeat_donors[parsed_line['DONOR_ID']] = parsed_line['TRANSACTION_DT']

        writer_output.close()

    except Exception as ex:
        template = "An exception of type {0} occurred in {1}"
        message = template.format(type(ex).__name__, str(ex))
        print message


def main(argv):
    """
        Main function to pass user entered inputs to function
        parse_file().
    """
    if len(argv) == 4:
        fn_itcont = argv[1]
        fn_pctl = argv[2]
        fn_output = argv[3]
        parsed_file = parse_file(fn_itcont, fn_pctl, fn_output)
        print fn_output + " is generated!"
    else:
        raise ValueError("Syntax error: inputs are not correct")


if __name__ == "__main__":
    try:
        main(sys.argv)
    except ValueError as err:
        print err
    # fn_itcont = "D:/Dropbox/insight_data_challenge/2018/insight_testsuite/tests/test_th2/input/itcont.txt"
    # fn_pctl = "D:/Dropbox/insight_data_challenge/2018/insight_testsuite/tests/test_th2/input/percentile.txt"
    # fn_output = "D:/Dropbox/insight_data_challenge/2018/insight_testsuite/tests/test_th2/output/repeat_donors_TH.txt"

    # parse_file(fn_itcont, fn_pctl, fn_output)


# handle input output file error