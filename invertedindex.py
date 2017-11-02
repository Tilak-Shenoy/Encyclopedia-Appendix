import string
#Main class
flag=''
class Index(object):
	#Constructor
	def __init__(self):
		self.inverted_index = {}
	#Formatting the data 
	def construct(self,file):
		l = 0
		with open(file) as f:
			content = f.readlines()
		content = [x.strip() for x in content] 
		for i in content:
			l += 1
			self.insert(l,i)
		print("Successfully Inserted!!!!")
	#inserting the data
	def insert(self,lineno,sentence):
		tokenise = lambda s : s.split()
		self.insert_tokens(lineno,tokenise(sentence))
	#inserting each word
	def insert_tokens(self,lineno,tokens):
		for token in tokens:
			z = isnormWord(token)
			if z == 2:
				continue
			elif z == 1:		
				if not token in self.inverted_index:
					self.inverted_index[token] = {}
					self.inverted_index[token][lineno] = 0
				if not lineno in self.inverted_index[token]:
					self.inverted_index[token][lineno] = 0
				self.inverted_index[token][lineno] += 1
			else:
				tokens.append(flag)
				self.insert_tokens(lineno,flag)
	#O(1) search
	def search(self,token):
		if token in self.inverted_index:
			print("LineNumber | Frequency:")
			return self.inverted_index[token]
		else:	
			return None
def display(x):
	try:
		for i in x:
			print(i,"   |   ",x[i])
	except Exception as e:
		print("Word not Found")
def isnormWord(a):
	invalidChars = set(string.punctuation.replace("_", ""))
	if a[len(a) - 1] in invalidChars:
		global flag
		flag=a[0:len(a)-1]
		return 0
	elif a in bad:
		return 2
	elif a[0] in invalidChars:
		flag=a[1:]
		return -1
	else:	
		return 1
bad = frozenset([
'a', 'about', 'across', 'after', 'afterwards', 'again', 
'against', 'all', 'almost', 'alone', 'along', 'already', 'also','although',
'always','am','among', 'amongst', 'amoungst', 'amount',  'an', 'and', 'another',
'any','anyhow','anyone','anything','anyway', 'anywhere', 'are', 'around', 'as',
'at', 'back','be','became', 'because','become','becomes', 'becoming', 'been', 
'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 
'between', 'beyond', 'bill', 'both', 'bottom','but', 'by', 'call', 'can', 
'cannot', 'cant', 'co', 'con', 'could', 'couldnt', 'cry', 'de', 'describe', 
'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 
'either', 'eleven','else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 
'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 
'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former', 
'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get',
'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 
'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself', 'him', 
'himself', 'his', 'how', 'however', 'hundred', 'ie', 'if', 'in', 'inc', 
'indeed', 'interest', 'into', 'is', 'it', 'its', 'itself', 'keep', 'last', 
'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 
'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly', 
'move', 'much', 'must', 'my', 'myself', 'name', 'namely', 'neither', 'never', 
'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 
'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only',
'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out',
'over', 'own','part', 'per', 'perhaps', 'please', 'put', 'rather', 're', 'same',
'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 
'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 
'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 
'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their', 
'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 
'therefore', 'therein', 'thereupon', 'these', 'they', 'thickv', 'thin', 'third',
'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 
'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 
'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 
'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter',
'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 
'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 
'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself',
'yourselves', 'the'])
i=Index() 
i.construct("a.txt")
print("Enter word to be searched!")
word = input()
display(i.search(word))
flag = None