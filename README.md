# Table of Contents
1. [Introduction](README.md#introduction)
2. [Environment](README.md#environment)
3. [How to run](README.md#how-to-run)
4. [Main files](README.md#main-files)
5. [Repo directory structure](README.md#repo-directory-structure)


# Introduction
This repo contains for Coding challenge of Insight's Data Engineering fellowship program. Please refer to https://github.com/InsightDataScience/donation-analytics for details.

# Environment
    1. Python 2.7.14
    2. Python modules needed: bisect, math, datetime, and sys

# Main files
    1. main.py: process political contribution data and generate an output file
    2. code_utility.py: contains utility code used by main.py
    3. itcont.txt: an input file with donation data
    4. percentile.txt: an input file with desired percentile value
    5. repeat_donors.txt: an output file with recipient ID,  zipcode, year, percentile of donations, total amount of donation, and total number of contributions (e.g., C00003251|45503|2018|4|1|4)

# How to run
  Once this repository is downloaded:
  
    1. run `run.sh` for the default example or 
    2. type the following command in terminal:
    `$ python ./src/main.py ./input/itcont.txt ./input/percentile.txt ./output/repeat_donors.txt`


# Repo directory structure

The directory structure for your repo should look like this:

    ├── README.md 
    ├── run.sh
    ├── data_dict.txt
    ├── src
    │   └── code_utility.py
    │   └── main.py
    ├── input
    │   └── percentile.txt
    │   └── itcont.txt
    ├── output
    |   └── repeat_donors.txt
    ├── insight_testsuite
        └── run_tests.sh
        └── tests
            └── test_1
            |   ├── input
            |   │   └── percentile.txt
            |   │   └── itcont.txt
            |   |__ output
            |   │   └── repeat_donors.txt
            ├── test_th
                ├── input
                │   └── percentile.txt
                │   └── itcont.txt
                |── output
                    └── repeat_donors.txt
