import PyPDF2
import time
import nltk
import re


def tokenize_tokens(text):
	return nltk.tokenize.word_tokenize(text)

def fold_case(tokens):
	return [tok.lower() for tok in tokens]

stopwords = nltk.corpus.stopwords.words('english')
def remove_stop_words(tokens):
	return [t for t in tokens if t.lower() not in stopwords]

stemmer = nltk.PorterStemmer()
def stem(tokens):
	return [stemmer.stem(t) for t in tokens]

def filter_tokens(tokens, min_size=0, special_chars=False):
	if min_size>0:
		tokens = [t for t in tokens if len(t) >= min_size]
	if special_chars:
		tokens = [t for t in tokens if re.search('[^a-zA-Z-]',t)==None]
	return tokens

def preprocess_text(text, do_stop_word_removal=True, do_stemming=True, fold=True, specials=True, min_size=3):
	ts = tokenize_tokens(text)
	ts = filter_tokens(ts, min_size=min_size,special_chars=specials)
	if fold:
		ts = fold_case(ts)
	if do_stop_word_removal:
		ts = remove_stop_words(ts)
	if do_stemming:
		ts = stem(ts)
	return ts



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
			x=preprocess_text(x)
			self.insert_tokens(i + 1,x)
		# closing the pdf file object
		pdfFileObj.close()

		print("Successfully Inserted!!!!")
	#inserting each word
	def insert_tokens(self,pageno,tokens):
		for token in tokens:
			if not token in self.inverted_index:
				self.inverted_index[token] = {}
				self.inverted_index[token][pageno] = 0
			if not pageno in self.inverted_index[token]:
				self.inverted_index[token][pageno] = 0
			self.inverted_index[token][pageno] += 1
	#O(1) search
	def search(self,token):
		token=token.lower()
		stemmer = nltk.PorterStemmer()
		token=stemmer.stem(token)
		if token in self.inverted_index:
			#print("PageNumber | Frequency:")
			#return self.inverted_index[token]
			return True
		else:	
			return False
			#return None
def display(x):
	try:
		for i in x:
			print('{:^6}{}{:3}'.format(i,'|',x[i]))
	except Exception as e:
		print("Word not Found")

def main():
	v=time.clock()
	i=Index() 
	i.construct("t.pdf")
	print(time.clock()-v)
	print("Enter word to be searched!")
	word = input()
	v=time.clock()
	print(i.search(word))
	#display(i.search(word))
	print(time.clock()-v)

if __name__ == '__main__':
	main()