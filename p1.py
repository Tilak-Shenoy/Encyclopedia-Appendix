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




class TrieNode:
	def __init__(self):
		self.children = [None]*27
		self.isEndOfWord = False
 
class Trie:
	def __init__(self):
		self.root = self.getNode()

	def getNode(self):
		return TrieNode()
 
	def _charToIndex(self,ch):
		if ch =='-':
			return 2
		else:         
			return ord(ch)-ord('a')
 
	def insert(self,key):
		pCrawl = self.root
		length = len(key)
		for level in range(length):
			index = self._charToIndex(key[level])
			if not pCrawl.children[index]:
				pCrawl.children[index] = self.getNode()
			pCrawl = pCrawl.children[index]
		pCrawl.isEndOfWord = True

	def search(self, key):
		pCrawl = self.root
		length = len(key)
		for level in range(length):
			index = self._charToIndex(key[level])
			if not pCrawl.children[index]:
				return False
			pCrawl = pCrawl.children[index]
 
		return pCrawl != None and pCrawl.isEndOfWord

def main():
	t=Trie()
	v=time.clock()
	pdfFileObj = open("t.pdf", 'rb')
	pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
	for i in range(pdfReader.numPages):
		pageObj = pdfReader.getPage(i)
		x = pageObj.extractText()
		x=preprocess_text(x)
		for key in x:
			t.insert(key)
	pdfFileObj.close()
	print(time.clock()-v)
	print("Successfully Inserted!!!!")
	print("Enter word to be searched!")
	word = input()
	v=time.clock()
	word = word.lower()
	stemmer = nltk.PorterStemmer()
	word=stemmer.stem(word)
	print(t.search(word))
	print(time.clock()-v)


if __name__ == '__main__':
	main()

