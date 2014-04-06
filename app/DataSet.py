import numpy
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

	def calcR(self, dataset):
		from scipy import stats
		return stats.pearsonr(self.data.values(), dataset.data.values())

	# Returns slope, intercept, r, p, stderr
	def linearRegression(self, dataset):
		from scipy import stats
		return stats.linregress(self.data.values(), dataset.data.values())
