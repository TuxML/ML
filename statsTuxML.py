#!/usr/bin/python3

import csv
import argparse

def stats(csvFilename):
    res = csv.reader(open(csvFilename))
    for row in res:
        print(row)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
        "Generates graphs and stuff about compilations from a CSV file")
    parser.add_argument("csv_filename", help="CSV file to read the data from")
    args = parser.parse_args()

    stats(args.csv_filename)

    