#!/usr/bin/python3

import csv
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


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

def graphInfo(tab1, tab2, title=""):
	plt.scatter(tab1, tab2)
	plt.title(title)
	return np.corrcoef(tab1, tab2)

def stats(csvFilename):
	"""Generation de statistiques sur les compilations effectuees :
	* Nombre de compilations
	* Informations sur les options activees en module
	* Informations sur les options activees en dur
	* Informations sur la taille des kernels generes
	* Informations sur le temps de compilation"""
	with open(csvFilename) as csvFile :
		reader = csv.DictReader(csvFile)
		
		nbLigne = 0
		nbM = {"Total": 0,"Min": 100000,"Max" : 0, "Mean" : 0}
		nbY = {"Total": 0,"Min": 100000,"Max" : 0, "Mean" : 0}
		nbMY = {"Total": 0,"Min": 100000,"Max" : 0, "Mean" : 0}
		kSize = {"Total": 0,"Min": 100000,"Max" : 0, "Mean" : 0}
		compTime = {"Total": 0,"Min": 100000,"Max" : 0, "Mean" : 0}
		tabCompTime = []
		tabSize = []
		tabY = []
		tabM = []
		tabActive = [] 
		
		for ligne in reader :
			nbLigne += 1
			tmpM = nbMinLine(ligne)
			tmpY = nbYinLine(ligne)
			ligne["KERNEL_SIZE"] = str(int(ligne["KERNEL_SIZE"]) / (2**20)) #Conversion de la taille du noyau en Mo
			tmpTime = float(ligne["COMPILE_TIME"])
			
			tabCompTime.append(tmpTime)
			tabSize.append(float(ligne["KERNEL_SIZE"]))
			tabY.append(tmpY)
			tabM.append(tmpM)
			tabActive.append(tmpM+tmpY)
			
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
		
		matplotlib.style.use('ggplot')
		
		coef1 = graphInfo(tabSize, tabCompTime, 'Temps de compilation en fonction de la taille du kernel')
		plt.show()
		print(coef1[0][1])
		
		plt.subplot(3,2,1)
		coef2 = graphInfo(tabActive, tabCompTime, 'Temps de compilation en fonction des options actives(y/m)')
		print(coef2[0][1])
		plt.subplot(3,2,2)
		coef3 = graphInfo(tabActive, tabSize, 'Taille du kernel en fonction des options actives(y/m)')
		print(coef3[0][1])
		
		
		plt.subplot(3,2,3)
		coef4 = graphInfo(tabY, tabCompTime, 'Temps de compilation en fonction des options actives(y)')
		print(coef4[0][1])
		plt.subplot(3,2,4)
		coef5 = graphInfo(tabY, tabSize, 'Taille du kernel en fonction des options actives(y)')
		print(coef5[0][1])
		
		
		plt.subplot(3,2,5)
		coef6 = graphInfo(tabM, tabCompTime, 'Temps de compilation en fonction des options actives(m)')
		print(coef6[0][1])
		plt.subplot(3,2,6)
		coef7 = graphInfo(tabM, tabSize, 'Taille du kernel en fonction des options actives(m)')
		print(coef7[0][1])
		
		plt.show()
		
		return (nbLigne, nbM, nbY, nbMY, kSize, compTime)

		

		
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description=
		"Generates graphs and stuff about compilations from a CSV file")
	parser.add_argument("csv_filename", help="CSV file to read the data from")
	args = parser.parse_args()

	statistiques = stats(args.csv_filename)
	print(statistiques)


