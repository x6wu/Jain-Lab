import urllib
import requests
import sys
import re
from html.parser import HTMLParser

#Inherited from Python built-in class 
class MyHTMLParser(HTMLParser):
	def __init__(self, list):
		HTMLParser.__init__(self)
		self.list = list
	def handle_data(self, data):
		if data.isspace() == False:
			self.list.append(data.strip())
	def getList(self):
		return self.list

def search(accessionID):
	dict={}
	list = []
	url = "http://spectra.psc.riken.jp/menta.cgi/respect/datail/datail?accession="
	fullUrl = url + accessionID
	request = urllib.request.Request(fullUrl)
	try:
		resp = urllib.request.urlopen(request)
		data = resp.read().decode("utf-8")
		filename = "ReSpectOutput" + accessionID + ".txt"
		file = open(filename, "w")
		findTable = re.compile('<div id="details".*?>(.*?)</div>',re.S)
		items = re.findall(findTable,data)
		data = listToString(items)
		parser = MyHTMLParser(list)
		parser.feed(data)
		parserList = parser.getList()
		inchiIndex = parserList.index("CH$  INCHI")
		massIndex = parserList.index("CH$  EXACT_MASS")
		if "PUBCHEM" in parserList:
			pubchemIndex = parserList.index("PUBCHEM")
		else:
			pubchemIndex = -1
		dict["exactMass"] = parserList[massIndex+1]
		dict["INCHI"] = parserList[inchiIndex+1]
		if(pubchemIndex == -1):
			dict["pubchemID"] = 'N/A'
		else:
			dict["pubchemID"] = parserList[pubchemIndex+1]
		print(dict)
		return dict

	except urllib.error.HTTPError as e:
		content = e.read()
		print(content)
		return False

def listToString(listToDo):
	string = ""
	for item in listToDo:
		string = string + item
	return string

def main(accessionID):
	search(accessionID)

if __name__ == '__main__':
	main(sys.argv[1])
