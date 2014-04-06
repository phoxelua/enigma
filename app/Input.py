import us
import requests
import json
import urllib2

#Dictionary of source-base urls
BASE = { "census" : "http://api.census.gov/data", "bea" : "http://www.bea.gov/api/data"}

#Dictionary of source-keys
KEYS = {"census" : "af52de2bd3b76ac873857b9ca728ccfe93b845b7", "bea" : "F2B4C8A5-1EB5-4E32-A2D8-F1041FEC9D24"}


#Dictionary of datatype-source
SOURCE = {"pop": "bea", "gdp": "bea", "corporate": "bea"}

#Dictionary of datatype-keycode
KEYCODES = {"pop" : "POP_SI", "gdp": "bea"} #IMPORTANT: MUST CONSIDER START YEARS TOO!

#Dictionary of appendix-datasetname
APPENDIX = {"pop": "RegionalData", "gdp": "NIPA", "corporate":"NIPA"}

class Input:
# http://api.census.gov/data/2010/sf1?key=af52de2bd3b76ac873857b9ca728ccfe93b845b7&get=P0010001,NAME&for=state:*
# http://api.census.gov/data/2011/acs5?key=af52de2bd3b76ac873857b9ca728ccfe93b845b7&get=B25070_003E,NAME&for=county:*&in=state:06

	def __init__(self, datatype1 ,datatype2, country1, country2, state1, state2, county1, county2, start, end): 
		self.datatype1 = datatype1 #to map source dict
		self.datatype2 = datatype2
		
		self.country1= country1
		self.country2 = country2

		self.state1 = state1
		self.state2 = state2

		self.county1 = county1
		self.county2 = county2

		self.start = start
		self.end = end

	def makeDictionary(self, type):
		if type == 1:
			return self.getallData(self.datatype1, self.country1, self.state1, self.county1, self.start, self.end)
		if type == 2:
			return self.getallData(self.datatype2, self.country2, self.state2, self.county1, self.start, self.end)
		print "INVALID TYPE!"

	def getallData(self, datatype, country, state, county, start,end):
		purl = self.buildPartialRequest(datatype, country, state, county)
		# print "Partial url for " + datatype + ": " + purl
		# print ""
		data = {}
		year = ""
		print "----Getting data for " + datatype + "----"
		for i in range(int(self.start), int(self.end)):
			year += str(i) + ','

		url = purl + year[:len(year)-1] + "&resultformat=json"	
		print url
		json = self.getJSON(datatype, url)
		print "JSON retrieved."

		for i in range(0, int(end) - int(start)):
			kv = self.getData(datatype, json, i)
			data[str(kv[0])] = float(kv[1].replace(",", ""))	
		print "----Done getting data."
		return data

	def getJSON(self, datatype, url):
		return requests.get(url).json()['BEAAPI']['Results']['Data']

	def getJSON2(self,url):
		data = urllib2.urlopen(url)
		return json.load(data)['BEAAPI']['Results']['Data']

	# Takes in JSON, return key-value 
	def getData(self, datatype, json, i):
		jsondata = json[i]
		entry = ""
		if datatype == "pop":
			entry = (jsondata['TimePeriod'], jsondata['DataValue'])	
		if datatype == "gdp":
			entry = (jsondata['TimePeriod'], jsondata['DataValue'])	
		if datatype == "corporate":
			entry = (jsondata['TimePeriod'], jsondata['DataValue'])	
		return entry

	# Build a partial url up to year 
	def buildPartialRequest(self, datatype, country, state, county):
		url = ""
		source = SOURCE[datatype]
		if source == "bea":
			if APPENDIX[datatype] == "RegionalData":
				url += BASE[source]  + "?&UserID=" + KEYS[source] + "&method=GETDATA&datasetname=RegionalData&keycode=" + KEYCODES[datatype] + "&geoFIPS=" + self.getFIPSCode(state) + "&year="
			elif APPENDIX[datatype] == "NIPA" and datatype == "gdp":
				url += BASE[source]  + "?&UserID=" + KEYS[source] + "&method=GETDATA&datasetname=NIPA&TableID=5&Frequency=A&Year="	
			elif APPENDIX[datatype] == "NIPA" and datatype == "corporate":
				url += BASE[source]  + "?&UserID=" + KEYS[source] + "&method=GETDATA&datasetname=NIPA&TableID=256&Frequency=A&Year="					
		return url

	#Return a string that represents the FIPS code of a state
	def getFIPSCode(self, state):
		return str(us.states.mapping('name', 'fips')[state]) + "000"
