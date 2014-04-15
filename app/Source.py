from abc import ABCMeta, abstractmethod
import us
import requests
import json
import urllib2

import hashlib
import os

from collections import namedtuple

class Source:
	__metaclass__ = ABCMeta

	@abstractmethod
	def makeDictionary(self):
		pass

	@abstractmethod
	def getData(self):
		pass


class BEASource(Source):

	name = "bea"

	base = "http://www.bea.gov/api/data?&UserID=F2B4C8A5-1EB5-4E32-A2D8-F1041FEC9D24" #cheat

	#mapping from dataSet to keyCodes
	dataSets = {"RegionalData": set(["RGDP_SP", "EMP000_SI", "TPI_SI", "POP_SI"]), "NIPA":set(["5", "111", "256"]), "NIUnderlyingDetail":set()}

	#mapping from uniput to tables
	tables = {"population": "POP_SI", "gdp": "5", "employment": "EMP000_SI", "income": "TPI_SI",
	"subsidies" : "111", "corporateprofit" : "256"
	}
	#CATION: start times do not match some for some tables
	
	#omg this is so ugly-bad i'm crying
	demoCache = {}


	def __init__(self):
		pass

	# Build a partial url up to year 
	def buildPartialRequest(self, subsource, table, selector, extra):
		purl = self.base + "&method=GETDATA&datasetname=" + subsource
		if subsource == "RegionalData":
			purl += "&keycode=" + table + "&geoFIPS=" + self.getFIPSCode(selector) 
		if subsource == "NIPA":
			purl += "&TableID=" + table + "&Frequency=A"# + extra #hard- nlp
		if subsource == "NIUnderlyingDetail":
			pass
		return purl

	#Return a string that represents the FIPS code of a state
	def getFIPSCode(self, state):
		return str(us.states.mapping('name', 'fips')[state]) + "000"

	def makeDictionary(self, query):
		name = hashlib.md5(str(str(query.table) + str(query.selectors) + str(int(query.start)) + str(int(query.end)))).hexdigest()
		print "file name: " + name
		try:
		 	os.path.isfile(name)
			print "Retrieving data..."
			with open(name) as json_file:
				json_data = json.load(json_file)
				# print(json_data)
			print "Retrieved."
			return json_data
		except IOError:
			print "Poop couldn't cache"
			purl = self.buildPartialRequest(query.subsource, query.table, query.selectors, query.extras)
			data = {}
			year = "&year="
			
			print "----Getting data for " + query.table + "----"
			for i in range(int(query.start), int(query.end)):
				year += str(i) + ","
			# should put cond in for to save splice time
			url = purl + year[:len(year)-1] + "&resultformat=json"
			
			print url

			# raise Exception("NO more JSON pls")

			jsondata = self.getJSON(url)
			print "JSON retrieved."
			for i in range(0, int(query.end) - int(query.start)):
				kv = self.getData(jsondata, i)
				data[str(kv[0])] = float(kv[1].replace(",", ""))
			print "Done getting data."

			#write to txt and update cache here
			print "Storing..."
			
			with open(name, "w") as outfile:
				json.dump(data, outfile, indent=4)

			# BEASource.demoCache[int(hashlib.md5(name).hexdigest(), 16)] = name
			print "Stored."
			return data


	def getJSON(self, url):
		return requests.get(url).json()['BEAAPI']['Results']['Data']

	def getJSON2(self,url):
		data = urllib2.urlopen(url)
		return json.load(data)['BEAAPI']['Results']['Data']

	def getData(self, json, i):
		jsondata= json[i]
		return (jsondata['TimePeriod'], jsondata['DataValue'])


# class CenSource(Source):

# 	name = "census"
# 	# http://api.census.gov/data/2011/acs5?key=af52de2bd3b76ac873857b9ca728ccfe93b845b7&get=B25070_003E,NAME&for=county:*&in=state:06

# 	base = "http://api.census.gov/data/"
# 	base = "http://www.bea.gov/api/data"
# 	# &UserID=F2B4C8A5-1EB5-4E32-A2D8-F1041FEC9D24" #cheat

# 	#mapping from dataSet to keyCodes
# 	#acs5 - 2010-2012
# 	dataSets = {"acs5": set(["RGDP_SP", "EMP000_SI", "TPI_SI", "POP_SI"]), "NIPA":set(), "NIUnderlyingDetail":set()}

# 	#mapping from uniput to tables
# 	tables = {"population": "POP_SI", "gdp": "RGDP_SP", "employment": "EMP000_SI", "income": "TPI_SI"}


# 	def __init__(self, api_url, api_key=asdf):
# 		pass
# 	    self.url = '%s?api_key=%s' % (api_url, api_key)
#         self.response = requests.get(self.url)
#         self.data = self.response.json()

# 	# Build a partial url up to year 
# 	def buildPartialRequest(self, subsource, table, selector, extra):
# 		purl = self.base + "&method=GETDATA&datasetname=" + subsource
# 		if subsource == "RegionalData":
# 			purl += "&keycode=" + table + "&geoFIPS=" + self.getFIPSCode(selector) 
# 		if subsource == "NIPA":
# 			purl += "&TableID=" + table + "&Frequency=" + extra #hard- nlp
# 		if subsource == "NIUnderlyingDetail":
# 			pass
# 		return purl

# 	#Return a string that represents the FIPS code of a state
# 	def getFIPSCode(self, state):
# 		return str(us.states.mapping('name', 'fips')[state]) + "000"

# 	def makeDictionary(self, query):
# 		purl = self.buildPartialRequest(query.subsource, query.table, query.selectors, query.extras)
# 		data = {}
# 		year = ""
		
# 		print "----Getting data for " + query.table + "----"
# 		for i in range(int(query.start), int(query.end)):
# 			year += str(i) + ","
# 		# should put cond in for to save splice time
# 		url = purl + year[:len(year)-1] + "&resultformat=json"
		
# 		print url
# 		json = self.getJSON(url)
# 		print "JSON retrieved."
# 		for i in range(0, int(query.end) - int(query.start)):
# 			kv = self.getData(json, i)
# 			data[str(kv[0])] = float(kv[1].replace(",", ""))
# 		print "Done getting data."
# 		return data

# 	def getJSON(self, url):
# 		return requests.get(url).json()['BEAAPI']['Results']['Data']

# 	def getJSON2(self,url):
# 		data = urllib2.urlopen(url)
# 		return json.load(data)['BEAAPI']['Results']['Data']

# 	def getData(self, json, i):
# 		jsondata= json[i]
# 		return (jsondata['TimePeriod'], jsondata['DataValue'])
#      