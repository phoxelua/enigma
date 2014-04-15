from Query import *

class Input:

	def __init__(self, box1, box2, start, end): 
		#do fancy nlp here- I will assume it is given as followss
		# lol tableTag is technically a selector for appendix
		self.selector1, self.tableTag1 = box1.split(" ")
		self.selector2, self.tableTag2 = box2.split(" ")

		# NLP stuffs
		self.extra1 = None
		self.extra2 = None

		self.start = float(start)
		self.end = float(end)

	def generateQueries(self, sources):
		q1 = None
		q2 = None

		for source in sources:
			#deal with q1
			if self.tableTag1 in source.tables.keys():
				table = source.tables[self.tableTag1]
				for k in source.dataSets.keys():
					if table in source.dataSets[k]:
						q1 = Query(source, k, table, self.selector1, self.extra1, self.start, self.end)
			
			#deal with q2
			if self.tableTag2 in source.tables.keys():
				table = source.tables[self.tableTag2]
				for k in source.dataSets.keys():
					if table in source.dataSets[k]:
						q2 = Query(source, k, table, self.selector2, self.extra2, self.start, self.end)
		return q1, q2
