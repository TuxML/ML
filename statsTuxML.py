#!/usr/bin/python3

import csv
import argparse
def nbMinLine(dico) :
	res = 0
	for i in dico :
		if dico[i] == "m" :
			res += 1
	return res

def nbYinLine(dico) :
	res = 0
	for i in dico :
		if dico[i] == "y" :
			res += 1
	return res

def stats(csvFilename):
	with open(csvFilename) as csvFile :
		reader = csv.DictReader(csvFile)
		nbLigne = 0
		nbM = {"Total": 0,"Min": 100000,"Max" : 0, "Mean" : 0}
		nbY = {"Total": 0,"Min": 100000,"Max" : 0, "Mean" : 0}
		nbMY = {"Total": 0,"Min": 100000,"Max" : 0, "Mean" : 0}
		kSize = {"Total": 0,"Min": 100000,"Max" : 0, "Mean" : 0}
		compTime = {"Total": 0,"Min": 100000,"Max" : 0, "Mean" : 0}
		for ligne in reader :
			nbLigne += 1
			tmpM = nbMinLine(ligne)
			tmpY = nbYinLine(ligne)
			ligne["KERNEL_SIZE"] = str(int(ligne["KERNEL_SIZE"]) / (2**20)) #Conversion de la taille du noyau en Mo
			tmpTime = float(ligne["COMPILE_TIME"])
			
			nbM["Total"] += tmpM
			if tmpM < nbM["Min"] :
				nbM["Min"] = tmpM
			if tmpM > nbM["Max"] :
				nbM["Max"] = tmpM
			
			nbY["Total"] += tmpY
			if tmpY < nbY["Min"] :
				nbY["Min"] = tmpY
			if tmpY > nbY["Max"] :
				nbY["Max"] = tmpY
			
			nbMY["Total"] += tmpM + tmpY
			if (tmpM + tmpY) < nbMY["Min"] :
				nbMY["Min"] = tmpM + tmpY
			if (tmpM + tmpY) > nbMY["Max"] :
				nbMY["Max"] = tmpM + tmpY
			
			kSize["Total"] += float(ligne["KERNEL_SIZE"])
			if float(ligne["KERNEL_SIZE"]) < kSize["Min"] :
				kSize["Min"] = float(ligne["KERNEL_SIZE"])
			if float(ligne["KERNEL_SIZE"]) > kSize["Max"] :
				kSize["Max"] = float(ligne["KERNEL_SIZE"])
			
			compTime["Total"] += tmpTime
			if tmpTime < compTime["Min"] :
				compTime["Min"] = tmpTime
			if tmpTime > compTime["Max"] :
				compTime["Max"] = tmpTime
							
		nbM["Mean"] = nbM["Total"]/nbLigne
		nbY["Mean"] = nbY["Total"]/nbLigne
		nbMY["Mean"] = nbMY["Total"]/nbLigne
		kSize["Mean"] = kSize["Total"]/nbLigne
		compTime["Mean"] = compTime["Total"]/nbLigne
		return (nbLigne, nbM, nbY, nbMY, kSize, compTime)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=
		"Generates graphs and stuff about compilations from a CSV file")
	parser.add_argument("csv_filename", help="CSV file to read the data from")
	args = parser.parse_args()

	statistiques = stats(args.csv_filename)
#	print(statistiques)


