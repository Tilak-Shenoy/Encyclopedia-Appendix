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



def custom_hash(key):
	"""
	Return the hash value of the given key. Uses dbj2
	@param key: String or unicode
	"""
	result = 5381
	multiplier = 33

	if isinstance(key, int):
		return key
	
	for char in key:
		result = 33 * result + ord(char)
	return result

class Hash(object):
	def __init__(self, size=10000, hashfunction=custom_hash):
		# Total block size which can be array or list
		self._size = size
		# Initial hashtable size
		self.__initial_size = self._size
		# Counter for holding total used slots
		self._used_slots = 0
		# Counter for holding deleted keys
		self._dummy_slots = 0
		# Holds all the keys
		self._keys = [None] * self._size
		# Holds all the values
		self._values = [None] * self._size
		# Alias for custom_hash function
		self.hash = hashfunction
		# threshold is used for increasing hash table
		self._max_threshold = 0.70
	
	def should_expand(self):
		"""Returns True or False
		
		If used slots and dummy slots are more than 70% resize the hash table.
		"""
		return (float(self._used_slots + self._dummy_slots) / self._size) >= self._max_threshold

	def _probing(self, current_position):
		"""Quadratic probing to get new position when collision occurs.
		@param current_position: position at already element is present.
		"""
		# Algorithm is copied from CPython http://hg.python.org/cpython/file/52f68c95e025/Objects/dictobject.c#l69
		return ((5 + current_position) + 1) % self._size
	
	def _set_item_at_pos(self, position, key, value):
		self._keys[position] = key
		self._values[position] = value
		
		self._used_slots += 1
		
	def _set_item(self, position, key, value):
		"""sets key and value in the given position.
		If position has already value in it, calls _probing to get next position
		@param position: index
		@param key: key
		@param value: value
		"""
		existing_key = self._keys[position]
		
		if existing_key is None or existing_key == key:
			# Empty or update
			self._set_item_at_pos(position, key, value)
		else:
			# Collision needs a probing. This needs to be recursive.
			new_position = self._probing(position)
			self._set_item(new_position, key, value)
		
	def _reposition(self, keys, values):
		"""Reposition all the keys and values.
		This is called whenever load factor or threshold has crossed the limit.
		"""
		for (key, value) in zip(keys, values):
			if key is not None:
				hashvalue = self.hash(key)
				position = self._calculate_position(hashvalue)
				
				self._set_item(position, key, value)
	   
	def _resize(self):
		old_keys = self._keys
		old_values = self._values
		
		# New size
		self._size = self._size * 4
		
		# create new block of memory and clean up old keys positions
		self._keys = [None] * self._size
		self._values = [None] * self._size
		self._used_slots = 0
		self._dummy_slots = 0
		
		# Now reposition the keys and values
		
		self._reposition(old_keys, old_values)
		
	def _calculate_position(self, hashvalue):
		return hashvalue % self._size
		
	def raise_if_not_acceptable_key(self, key):
		if not isinstance(key, (str, int)):
			raise TypeError("Key should be int or string or unicode")
		
	def put(self, key, value):
		"""Given a key and value add to the hashtable.
		Key should be int or string or unicode.
		"""
		self.raise_if_not_acceptable_key(key)
		
		if self.should_expand():
			self._resize()
			
		position = self._calculate_position(self.hash(key))
		self._set_item(position, key, value)
	
	def search(self,key):
		position = self._calculate_position(self.hash(key))
		existing_key = self._keys[position]
		if existing_key == key:
			return True		
		else:
			while(1):
				position = self._probing(position)
				existing_key = self._keys[position]
				if existing_key == key:
					return True
				if existing_key == None:
					break
					return False

	def _get_pos_recursively(self, position, key):
		new_position = self._probing(position)
		tmp_key = self._keys[new_position]
		
		if tmp_key == None:
			# At new position the key is empty raise ane exception
			raise KeyError(u"{} key not found".format(key))
		elif tmp_key != key:
			# Again check for next position
			return self._get_pos_recursively(new_position, key)
		else:
			return new_position
		
	def _get_pos(self, key):
		"""
		Returns position of the key
		"""
		self.raise_if_not_acceptable_key(key)
		position = self._calculate_position(self.hash(key))
		
		tmp_key = self._keys[position]

		if tmp_key == None:
			raise KeyError("{} doesn't exist".format(key))
			
		elif tmp_key != key:
			# Probably collision and get next position using probing
			return self._get_pos_recursively(position, key) 
		else:
			return position
		
	def get(self, key):
		position = self._get_pos(key)

		if position is None:
			return None
		
		return self._values[position]
	
	def _delete_item(self, position, key):
		self._keys[position] = None
		self._values[position] = None
		
		self._dummy_slots += 1
		
	def delete(self, key):
		"""Deletes the key if present. KeyError is raised if Key is missing.
		"""
		position = self._get_pos(key)
		
		if position is None:
			raise KeyError(key)
			
		self._delete_item(position, key)
		
	# Downsizing of hash map is not yet implemented. 



#Main class
class Index(object):
	#Constructor
	def __init__(self):
		self.inverted_index = Hash()
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
			if not self.inverted_index.search(token):
				ptr=Hash(2100)
				self.inverted_index.put(token,ptr)
				self.inverted_index.get(token).put(pageno,0)
			if not self.inverted_index.get(token).search(pageno):
				self.inverted_index.get(token).put(pageno,0)
			f=self.inverted_index.get(token).get(pageno)
			f+=1
			self.inverted_index.get(token).put(pageno,f)
	#O(1) search
	def search(self,token):
		token=token.lower()
		stemmer = nltk.PorterStemmer()
		token=stemmer.stem(token)
		if self.inverted_index.search(token):
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