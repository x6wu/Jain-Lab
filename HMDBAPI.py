import urllib
import requests
import sys
import re
import ReSpectAPI

def main(HMDBID):
	#http://www.hmdb.ca/metabolites/HMDB32243
	url = "http://www.hmdb.ca/metabolites/HMDB"
	fullUrl = url + HMDBID
	try:
		request = urllib.request.Request(fullUrl)
		resp = urllib.request.urlopen(request)
		data = resp.read().decode("utf-8",'ignore')
		# filename = 'HMDB '+HMDBID
		# file = open(filename, 'w')
		pattern1 = '</td></tr><tr><th>Monoisotopic Molecular Weight.*?(.*?)</td></tr><tr><th>'
		findDetails = re.compile(pattern1,re.S)
		exactMass = re.findall(findDetails,data)
		exactMass = ReSpectAPI.listToString(exactMass)
		exactMass = exactMass.split('<td>',1)[1]
		# file.write(exactMass)
		pattern2 = '</td></tr><tr><th>PubChem Compound.*?(.*?)<span class="glyphicon glyphicon-new-window">'
		findDetails = re.compile(pattern2,re.S)
		pubChem = re.findall(findDetails,data)
		pubChem = ReSpectAPI.listToString(pubChem)
		#Pubchem ID is not available i.e. HMDB56678
		# print(pubChem)
		# print(len(pubChem))
		if len(pubChem) == 0:
			pubChem = 'N/A'
		else:
			pubChem = pubChem.split('">',1)[1]
			pubChem = pubChem.strip()
		# file.write(pubChem)
		pattern3 = '</td></tr><tr><th>InChI Key.*?(.*?)</td></tr><tr id="taxonomy">'
		findDetails = re.compile(pattern3,re.S)
		inChiKey = re.findall(findDetails,data)
		inChiKey = ReSpectAPI.listToString(inChiKey)
		try:
			inChiKey = inChiKey.split('=',1)[1]
		except:
			inChiKey = 'N/A'
		# file.write(inChiKey)
		# file.close()
		dict = {}
		dict["exactMass"] = exactMass
		dict["InChIKey"] = inChiKey
		dict["pubchemID"] = pubChem
		print(dict)
		return dict
	except urllib.error.HTTPError as exception:
		print(str(exception.code) + ' ' + exception.reason)
		return False


if __name__ == '__main__':
	main(sys.argv[1])