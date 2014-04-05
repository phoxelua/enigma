# import numpy
import scipy

class DataSet:
	
	def __init__(self, data):
		self.data = data #dictionary of t-x
		# self.schema = 
		self.mean = self.calcMean()  
		self.std = self.calcStd()

	def calcMean(self):
		return scipy.nanmean(self.data.values())

	def calcStd(self):
		return scipy.nanstd(self.data.values())