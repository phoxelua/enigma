from Input import * 
from DataSet import *

if __name__ == "__main__":

	data1 = "pop"
	data2 = "pop"
	country1 = "us"
	country2 = "us"
	state1 = "Florida"
	state2 = "New York"
	county1 = ""
	county2 = ""
	start = "1991"
	end = "2006"


	uinput = Input(data1 ,data2, country1, country2, state1, state2, county1, county2, start, end)
	d1 = DataSet(uinput.makeDictionary(1))

	print d1.data

	d2 = DataSet(uinput.makeDictionary(2))

	print d2.data
	
	r = d1.calcR(d2)

	print r 
