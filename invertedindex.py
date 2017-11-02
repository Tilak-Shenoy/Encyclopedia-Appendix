class Index(object):
	def __init__(self):
		self.inverted_index = {}
	def construct(self,file):
		l = 0
		with open(file) as f:
			content = f.readlines()
		content = [x.strip() for x in content] 
		for i in content:
			l += 1
			print(i)
			print()
			self.insert(l,i)
	def insert(self,lineno,sentence):
		tokenise = lambda s : s.split()
		self.insert_tokens(lineno,tokenise(sentence))
	def insert_tokens(self,lineno,tokens):
		for token in tokens:
			if not token in self.inverted_index:
				self.inverted_index[token] = {}
				self.inverted_index[token][lineno] = 0
			if not lineno in self.inverted_index[token]:
				self.inverted_index[token][lineno] = 0
			self.inverted_index[token][lineno] += 1
	def search(self,token):
		if token in self.inverted_index:
			return self.inverted_index[token]
		else:
			return False
i=Index()
i.construct("a.txt")
print(i.search('file'))

				