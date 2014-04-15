
class Query:

	def __init__(self, source, subsource, table, selectors, extras=None, start=None, end=None):
		self.source = source
		self.subsource = subsource
		self.selectors = selectors
		self.table = table
		self.extras = extras
		self.start = start
		self.end = end

	def toString(self):
		return "[ " + self.source.name + ", " + str(self.subsource) + ", " + str(self.table) + ", " + str(self.selectors) + ", " +str(self.extras) + ", " + str(self.start) + ", " + str(self.end) + " ]"