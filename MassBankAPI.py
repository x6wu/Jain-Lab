import sys
import suds
from suds.client import Client
import string

def main(MassBankID):
	url = 'http://www.massbank.jp/api/services/MassBankAPI?wsdl'
	try:
		client = Client(url)
		resp = client.service.getRecordInfo(MassBankID)
		data = str(resp)
		data = data.split('\n')
		dict={}
		for detail in data:
			if "CH$EXACT_MASS:" in detail:
				dict["exactMass"] = detail.split("EXACT_MASS: ",1)[1]
			elif "PUBCHEM" in detail:
				dict["pubchemID"] = detail.split("PUBCHEM ",1)[1]
			elif "InChI" in detail:
				dict["InChi"] = detail.split("InChI=",1)[1]
			return dict
	except suds.WebFault as exception:
		print(str(exception))
		return False


if __name__ == '__main__':
	main(sys.argv[1])