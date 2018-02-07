#!/usr/bin/python3

import csv
import argparse

def stats(csvFilename):
    with open(csvFilename) as csvFile :
        reader = csv.DictReader(csvFile)
        nbLigne = 0
        for ligne in reader :
            nbLigne += 1
            
            ligne['KERNEL_SIZE'] = str(int(ligne['KERNEL_SIZE']) / (2**10))
#            print(ligne['KERNEL_SIZE'])
        return (nbLigne)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=
        "Generates graphs and stuff about compilations from a CSV file")
    parser.add_argument("csv_filename", help="CSV file to read the data from")
    args = parser.parse_args()

    stats(args.csv_filename)
    

    
