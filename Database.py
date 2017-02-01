import sqlite3
import sys
import os.path
import csv

def main(filepath):
	global connection
	connection = sqlite3.connect(filepath)
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

def add(spectrumID, compound, dataCollector, adduct, libMZ, PI, LMID, InchiKey, InchiCode, CID, mass1, mass2):
	try:
		with connection:
			if len(LMID) == 0:
				LMID = "N/A"
			connection.execute('''INSERT INTO \
				Compounds (SpectrumID, "Compound_Name","Data_Collector",Adduct,\
				LibMZ,PI,LMID,InChIKey,InChICode,"Pubchem CID", \
				"Monoisotopic Theoretical Mass","Theoretical Mass Of Adduct")VALUES\
				(?,?,?,?,?,?,?,?,?,?,?,?)''',\
				(spectrumID,compound,dataCollector,adduct,libMZ,PI,LMID,InchiKey,InchiCode,CID,mass1,mass2))
		print("data stored successfully")
	except sqlite3.IntegrityError:
		print("Compound with Spectrum ID " + spectrumID + " already exists") 
#TODO
def find(spectrumID):
	t = str(spectrumID)
	cursor.execute("SELECT * FROM Compounds where SpectrumID = ?",(t,))
	match = cursor.fetchone()
	str_match = str(match)
	if("None" in str_match):
		print("Such compound with SpectrumID " + spectrumID + " does not exsit")
		return False
	else:
		print(match)
		dict = {}
		dict["SpectrumID"] = match[0]
		dict["Compound_Name"] = match[1]
		dict["Data_Collector"] = match[2]
		dict["Adduct"] = match[3]
		dict["LibMZ"] = match[4]
		dict["PI"] = match[5]
		dict["LMID"] = match[6]
		dict["InChIKey"] = match[7]
		dict["InChICode"] = match[8]
		dict["Pubchem CID"] = match[9]
		dict["Monoisotopic Theoretical Mass"] = match[10]
		dict["Theoretical Mass Of Adduct"] = match[11]
		return dict

if __name__ == '__main__':
	main()
	connection.commit()
	connection.close()
