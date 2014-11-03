import os
import sys
import time
import nltk
import util 
import math
import pprint as pp
from collections import Counter, deque
from Parser import Parser

def init( directory ):
	if not os.path.exists( directory ) :
		os.makedirs( directory )
		print directory + ' created'
		
def readFile( name ) :
	with open( name, 'r' ) as f :
		return f.read().splitlines()

def writeFile( name, content ) :
	with open( name, 'w' ) as f :
		f.write( content )

def wordProcess( lst ) :
	parser = Parser()
	termString = parser.clean( lst )
	termLst = parser.tokenize( termString )
	termLst = parser.removeStopWords( termLst ) 
	termLst = util.removeDuplicates( termLst ) 
	return termLst

def numOfDocs( word, docList ) :
	count = 0 
	for doc in docList :
		if doc.split( ' ' ).count(word) > 0 :
			count = count + 1
	return count 

def idf( word, docList ) :	
	return math.log(len(docList))/numOfDocs( word, docList )

def output( lst, name ) :
	output = ( '::'.join([lst[i], str(i)]) for i in range( 0, len(lst) ) )

	writeFile('./block_data/'+name+'2num', '\n'.join(output) )

	output2 = ( ' '.join(['0', str(i)+':1']) for i in range(0, len(lst)) ) 
	writeFile( './block_data/'+name, '\n'.join(output2) )

if __name__ == '__main__' :
	if len(sys.argv) == 2 :
		isTF = '0'
		print 'word weighted in 1 and 0'

	elif len(sys.argv) == 3 and sys.argv[2] == '-tfidf' :
		isTF = '1'
		print 'word weighted in tf-idf'
	else :
		print 'Incorrect argument.'
		sys.exit()

	init('./block_data')

	pairs = readFile( sys.argv[1] )
	items = set()
	users = set()
	total_words = set()
	dict_user = dict() #the words which mapping to user
	dict_item = dict() #the words which mapping to item

	for pair in pairs :
		element = pair.split( '::' ) 
		items.add(element[0])
		users.add(element[1])

		procWord = wordProcess(element[0])
		procString = ' '.join(procWord)

		if dict_user.get(element[1]) is None :
			dict_user.update( {element[1]:procString} )
			total_words = total_words.union( set(procWord) )
		else :
			tmp = ' '.join({str(dict_user.get(element[1])), procString})
			dict_user.update( {element[1]:tmp} )

		if dict_item.get(element[0]) is None :
			dict_item.update( {element[0]:procString} )

#	pp.pprint( total_words, indent=4 )

	item_lst = list(items)
	user_lst = list(users)
	twords = list(total_words)

	iid = output( item_lst, 'rel-iid' )
	uid = output( user_lst, 'rel-uid' )
	wid = output( twords, 'rel-wid' )

	iid_data = deque() # rel-iid.data
	uid_data = deque() # rel-uid.data
	uwid_data = deque() # rel-uwid.data
	iwid_data = deque() # rel-iwid.data
	ans = deque()	# ans.data

	mapping_user = []
	mapping_count = deque()	#rel-wid
	mapping = deque()

	idf_user = dict()
	idf_item = dict()

	for text in total_words :
		idf_user.update( {text:str(idf(text, dict_user.values()))} )
		idf_item.update( {text:str(idf(text, dict_item.values()))} )

	for key in dict_user.keys():
		if isTF is '1':
			#tf
			tf = Counter( dict_user.get(key).split(' ') )
	
			tmp = []
			for text in tf.keys():
				if text in total_words:
					tmp.append( str(twords.index(text))+':'+str(float(tf.get(text))*float(idf_user.get(text))))
	
		else:
			clear_word = set(dict_user.get(key).split(' '))
		
			tmp = []
			for word in clear_word :
				if word in total_words:
					tmp.append( str(twords.index(word))+':1' )
	
		mapping_count.append( '0 '+' '.join(tmp) )
		mapping_user.append( key )
		mapping.append( key+'::'+' '.join(tmp) )

	writeFile( './block_data/mapping', '\n'.join(mapping) )
	writeFile( './block_data/rel-uwid', '\n'.join(mapping_count))

	mapping_item = []
	mapping_icount = deque()
	mapping_i = deque()

	for key in dict_item.keys():
		if isTF is '1':
			#tf
			tf = Counter(dict_item.get(key).split(' '))
			tmp = []
			for text in tf.keys():
				if text in total_words:
					tmp.append( str(twords.index(text))+':'+str(float(tf.get(text))*float(idf_item.get(text))) )
	
		else:
			clear_word = set(dict_item.get(key).split(' '))
		
			tmp = []
			for word in clear_word :
				if word in total_words :
					tmp.append( str(twords.index(word))+':1' )
	
		mapping_icount.append( '0 '+' '.join(tmp) )
		mapping_item.append( key )
		mapping_i.append( key+'::'+' '.join(tmp) )

	writeFile( './block_data/mapping_i', '\n'.join(mapping_i) )
	writeFile( './block_data/rel-iwid', '\n'.join(mapping_icount) )

	for pair in pairs:
		elements = pair.split( '::' )
		iid_data.append(str(item_lst.index(elements[0])))
		uid_data.append(str(user_lst.index(elements[1])))
		uwid_data.append(str(mapping_user.index(elements[1])))
		iwid_data.append(str(mapping_item.index(elements[0])))
		ans.append(str(elements[2]))

	writeFile( './block_data/rel-iid.data', '\n'.join(iid_data) )
	writeFile( './block_data/rel-uid.data', '\n'.join(uid_data) )
	writeFile( './block_data/rel-uwid.data', '\n'.join(uwid_data) )
	writeFile( './block_data/rel-iwid.data', '\n'.join(iwid_data) )
	writeFile( './block_data/ans.data', '\n'.join(ans) )

