import sqlite3
import sys
import os.path
import csv
import GNPSAPI
import NIST14API
import pubchempy

class MyCompound():
	#spectrumID,compound,dataCollector,adduct,libMZ,PI,LMID,Key,InchiCode,CID,mass1,mass2
	def __init__(self):
		self.spectrumID = ''
		self.name = ''
		self.dataCollector = ''
		self.adduct = ''
		self.libMZ = ''
		self.LMID = ''
		self.InchiKey = ''
		self.InchiCode = ''
		self.CID = ''
		self.exactMass = ''
		self.adductMass = ''
		self.PI = ''
	def setPI(self, PI):
		self.PI = PI
	def setName(self, name):
		self.name = name
	def setSpectrumID(self, spectrumID):
		self.spectrumID = spectrumID
	def setDataCollector(self, dataCollector):
		self.dataCollector = dataCollector
	def setAdduct(self, adduct):
		self.adduct = adduct
	def setLibMZ(self, libMZ):
		self.libMZ = libMZ
	def setLMID(self, LMID):
		self.LMID = LMID
	def setInchiKey(self, InchiKey):
		self.InchiKey = InchiKey
	def setInchi(self, Inchi):
		self.Inchi = Inchi
	def setCID(self, CID):
		self.CID = CID
	def setExactMass(self, exactMass):
		self.exactMass = exactMass
	def setAdductMass(self, adductMass):
		self.adductMass = adductMass
	def getName(self):
		return self.name
	def getSpectrumID(self):
		return self.spectrumID
	def getDataCollector(self):
		return self.dataCollector
	def getAdduct(self):
		return self.adduct
	def getLibMZ(self):
		return self.libMZ
	def getLMID(self):
		return self.LMID
	def getInchiKey(self):
		return self.InchiKey
	def getInchi(self):
		return self.Inchi
	def getCID(self):
		return self.CID
	def getExactMass(self):
		return self.exactMass
	def getAdductMass(self):
		return self.adductMass
	def getPI(self):
		return self.PI

def read(filename):
	#filename = 'GNPS-EMBL-MCF.mgf'
	file = open(filename, 'r')
	lines = file.readlines()
	compounds = []
	count = 0
	for line in lines:
		if(line.startswith('BEGIN IONS')):
			count = count + 1
			currCompound = MyCompound()
		if(line.startswith('PEPMASS=')):
			currLibMZ = line.rsplit('=',1)[1]
			currCompound.setLibMZ(currLibMZ)
		if(line.startswith('PI=')):
			currPI = line.rsplit('=',1)[1]
			currCompound.setPI(currPI)
		if(line.startswith('DATACOLLECTOR=')):
			currCollector = line.rsplit('=',1)[1]
			currCompound.setDataCollector(currCollector)
		if(line.startswith('NAME=')):
			currAdduct = line.rsplit(' ',1)[1]
			currCompound.setAdduct(currAdduct)
			currName = line.rsplit(' ',1)[0]
			currName = currName.strip()
			currName = currName.split('=',1)[1]
			currName = currName.strip('"')
			currCompound.setName(currName)
		if(line.startswith('INCHI=')):
			currInchi = line.split('INCHI=',1)[1]
			currInchi = currInchi.strip()
			currInchi = currInchi.strip('"')
			currCompound.setInchi(currInchi)
		if(line.startswith('INCHIAUX=')):
			currInchiKey = line.rsplit('=',1)[1]
			currCompound.setInchiKey(currInchiKey)
		if(line.startswith('SPECTRUMID=')):
			currSpectrumID = line.rsplit('=',1)[1]
			currCompound.setSpectrumID(currSpectrumID)
		if(line.startswith('PUBMED=')):
			currCID = line.rsplit('=',1)[1]
			currCompound.setCID(currCID)
		if(line.startswith('END IONS')):
			compounds.append(currCompound)
			count = count + 1
	file.close()
	if(count == len(compounds)):
		print("finish reading file")
	return compounds

def searchInchi():
	#TODO
	pass

def search(compoundList):
	for compound in compoundList:
		print('new compound: ' + compound.getName())
		exactMass = ''
		if(compound.getInchi() == 'N/A'):
			exactMass = NIST14API.ChemSpiderSearch(compound.getName())
			compound.setExactMass(exactMass)
		elif(compound.getInchi() == ''):
			exactMass = NIST14API.ChemSpiderSearch(compound.getName())
			compound.setExactMass(exactMass)
		else:
			try:
				print(compound.getInchi())
				exactMass = GNPSAPI.ChemSpiderSearchInchi(compound.getInchi())
				compound.setExactMass(exactMass)
			except Exception as e:
				compound.setExactMass('Manuel')
	return compoundList

def main(inputfile, databasePath):
	global connection
	connection = sqlite3.connect(databasePath)
	global cursor
	cursor = connection.cursor()
	#initialize table
	try:
		cursor.execute("""CREATE TABLE IF NOT EXISTS Compounds\
			(SpectrumID TEXT PRIMARY KEY,"Compound_Name" TEXT,"Data_Collector" TEXT,Adduct TEXT,\
			LibMZ TEXT,PI TEXT,LMID TEXT,InChIKey TEXT,InChICode TEXT,"Pubchem CID" TEXT, \
			"Monoisotopic Theoretical Mass" TEXT,"Theoretical Mass Of Adduct" TEXT)""")
		print("table created lol")
		connection.commit()
	except Exception as e:
		print("table already exists")
	compoundList = read(inputfile)
	newList = search(compoundList)
	for compound in newList:
		try:
			print('try to insert')
			connection.execute('''INSERT INTO \
				Compounds (SpectrumID, "Compound_Name","Data_Collector",Adduct,\
				LibMZ,PI,LMID,InChIKey,InChICode,"Pubchem CID", \
				"Monoisotopic Theoretical Mass","Theoretical Mass Of Adduct")VALUES\
				(?,?,?,?,?,?,?,?,?,?,?,?)''',\
				(compound.getSpectrumID(),compound.getName(),compound.getDataCollector(),\
				compound.getAdduct(),compound.getLibMZ(),compound.getPI(),compound.getLMID(),\
				compound.getInchi(),compound.getInchiKey(),compound.getCID(),compound.getExactMass(),\
				compound.getAdductMass()))	
			connection.commit()
			print("data stored successfully")
		except sqlite3.IntegrityError:
			print("Compound already exists") 
	connection.close()

if __name__ == '__main__':
	main(sys.argv[1], sys.argv[2])