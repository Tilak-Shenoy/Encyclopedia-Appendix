class Index(object):
	def __init__(self):
		self.inverted_index = Dict()
	def construct(self,file):
		f = open(file,'r')
		l = 0
		for i in f:
			l += 1
			self.insert(l,i)
	def insert(self,lineno,sentence,tokenise = lambda s : s.split()):
		self.insert_token(lineno,tokenise(sentence))
	def insert_tokens(self,lineno,tokens):
		for token in tokens:
			if not token in self.inverted_index:
				