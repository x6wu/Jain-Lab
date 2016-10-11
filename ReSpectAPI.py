import urllib
import json
import requests
import sys
import re
from html.parser import HTMLParser
from bs4 import BeautifulSoup

global list
list = []
#Straight copying from Python doc
class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
    	pass

    def handle_endtag(self, tag):
    	pass

    def handle_data(self, data):
    	if data.isspace() == False:
    		list.append(data.strip())
    		print("Encountered some data  :", data.strip())

def main(accessionID):
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
		#seems to work lol 
		parser = MyHTMLParser()
		parser.feed(data)

		inchiIndex = list.index("CH$  INCHI")
		massIndex = list.index("CH$  EXACT_MASS")
		pubchemIndex = list.index("PUBCHEM")
		dict={}
		dict["exactMass"] = list[massIndex+1]
		dict["INCHI"] = list[inchiIndex+1]
		dict["pubchemID"] = list[pubchemIndex+1]
		return dict

	except urllib.error.HTTPError as e:
		content = e.read()
		print(content)

def listToString(list):
	string = ""
	for item in list:
		string = string + item
	return string

if __name__ == '__main__':
	main(sys.argv[1])
