import string
import PyPDF2
import time
#Main class
class Index(object):
	#Constructor
	def __init__(self):
		self.inverted_index = {}
	#Formatting the data 
	def construct(self,file):
		# creating a pdf file object
		pdfFileObj = open(file, 'rb')
 
		# creating a pdf reader object
		pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
 
		# creating a page object
		for i in range(pdfReader.numPages):

			pageObj = pdfReader.getPage(i)
 
		# extracting text from page
			x = pageObj.extractText()
			x = x.split()
			print(x)
			self.insert_tokens(i + 1,x)
		# closing the pdf file object
		pdfFileObj.close()

		print("Successfully Inserted!!!!")
	#inserting each word
	def insert_tokens(self,pageno,tokens):
		for token in tokens:
			token = token.lower()
			if not token in bad: 
				if not token in self.inverted_index:
					self.inverted_index[token] = {}
					self.inverted_index[token][pageno] = 0
				if not pageno in self.inverted_index[token]:
					self.inverted_index[token][pageno] = 0
				self.inverted_index[token][pageno] += 1
			else:
				continue
	#O(1) search
	def search(self,token):
		if token in self.inverted_index:
			print("PageNumber | Frequency:")
			return self.inverted_index[token]
		else:	
			return None
def display(x):
	try:
		for i in x:
			print(i,"         |   ",x[i])
	except Exception as e:
		print("Word not Found")
bad = frozenset([
'a','righanglejaipur@gmail.com,', 'about', 'across', 'after', 'afterwards', 'again', 
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

v=time.clock()
i=Index() 
i.construct("c.pdf")
print(time.clock()-v)
print("Enter word to be searched!")
word = input().lower()
v=time.clock()
display(i.search(word))
print(time.clock()-v)