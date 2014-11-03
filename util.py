import sys
from sets import Set
from collections import Counter

#http://www.scipy.org/
try:
	from numpy import dot
	from numpy.linalg import norm
except:
	print "Error: Requires numpy from http://www.scipy.org/. Have you installed scipy?"
	sys.exit() 

def removeDuplicates(list):
	""" remove duplicates from a list """
	return Set((item for item in list))


def cosine(vector1, vector2):
	""" related documents j and q are in the concept space by comparing the vectors :
		cosine  = ( V1 * V2 ) / ||V1|| x ||V2|| """
	return float(dot(vector1,vector2) / (norm(vector1) * norm(vector2)))

def jaccard( vector1, vector2 ):
	union = 0
	intersection = 0
	
	for i in range( 0, len(vector1) ) :
		if vector1[i] != 0 and vector2[i] != 0 :
			union += 1
		elif vector1[i] != 0 or vector2[i] != 0 :
			intersection += 1
	return float(union)/intersection if union != 0 else 0  
		 	
