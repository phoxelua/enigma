from Input import * 
from DataSet import *

if __name__ == "__main__":

	data1 = "pop"
	data2 = "pop"
	country1 = "us"
	country2 = "us"
	state1 = "California"
	state2 = "New York"
	county1 = ""
	county2 = ""
	start = "1993"
	end = "2013"


	uinput = Input(data1 ,data2, country1, country2, state1, state2, county1, county2, start, end)
	d1 = DataSet(uinput.makeDictionary(1))

	print d1.data

	d2 = DataSet(uinput.makeDictionary(2))


	print d2.data
	# d1.correlate(d2)
