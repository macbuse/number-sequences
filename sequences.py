#calculate the orbit of the number 1 according to the rule
#x_0 = number of letters in the word for  1
#x_{n+1} = number of letters in the word  for x_n

#this is an early version

def chain(digits ):
	xx = [len(x) for x in digits]
	cur = xx[0]
	L = []
	while cur not in L:
		L.append(cur)
		cur = xx[cur -1]
	L.append(cur)
	
	return L



import re, urllib2, codecs,sys
import pickle
import string


########################################################################
#http://fredericiana.com/2010/10/08/decoding-html-entities-to-text-in-python/
import HTMLParser
h = HTMLParser.HTMLParser()

import htmlentitydefs, re

def convert(mystring):
	return re.sub('&([^;]+);', lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), mystring)

########################################################################


#strategy for utf8
#1/ open txt files  with the codecs.open command
#2/ use ur'''....''' with strings
UTF8Writer = codecs.getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

def read_lks():
	def filter_lks(x):
		if x[:4] == 'http': return False
		if x[0] not in string.lowercase : return False
		return True
	
	#I saved http://omniglot.com/language/numbers to disk first 
	fp = file('num_index.htm', 'r')
	lks = re.compile('<a href="(.*?)"')
	mm = lks.findall(fp.read())
	return [x for x  in mm if filter_lks(x) ][1:]
	

def read_from_web():
	tp = re.compile('<title>Numbers in (.*)?</title>')
	pp = re.compile(ur'>(\d+)</td>.*?<td>(.*?)<',re.DOTALL)
		
	lks = read_lks()
	numbers = {}
	
	for lk in lks[:]:
		print 'doing ' + lk
		try: 
			fp = urllib2.urlopen('http://omniglot.com/language/numbers/'+lk)
			data = fp.read()
		except:
			'page %s not found'%lk
			continue
		
		try:
			lang = tp.findall(data)
			
			nums  = pp.findall(data)
		except:
			'page %s contains no numbers'%lk
			continue
		
		language = lk[:-4]
		numbers[language] = nums
		

	fp = file('lang.pkl','wb')
	pickle.dump(numbers,fp)
	fp.close()


def get_lengths():
	fp = file('lang.pkl','r')
	nums = pickle.load(fp)
	
	languages = nums.keys()
	
	filtered_nums = {}
	languages.sort()
	num_nums = 20
	for language in languages:
		#the yiddish  page uses spans spo skip
		if language in ['vietnamese', 'yiddish']: continue
		
		if not nums[language]: continue
		print language
		
		first, char =  nums[language][0]
		if first =='0':
			digits = nums[language][1: num_nums + 1]
		else:
			digits = nums[language][:num_nums]
		digits =  [ h.unescape(y) for x,y in digits]
		if sum( len(x) for x in digits[:5]) < 6 :
			print language, 'is pictograms'
			continue
		
		lengths = []
		for i,y in enumerate(digits):
			#now there are a ton of filters to take out punctuation etc
			y = re.sub(r'\(.*?\)','',y)
			y = re.sub(r'\[.*?\]','',y)
			y = y.split(',')[0]
			y = y.split('/')[0]
			y = re.sub(r'\-|\*|\)','',y)
			#careful with teens!
			if i < 10:
				y = y.split(' ')[0]
			else:
				y = y.replace(' ','')
			y = y.strip()
			print   i+1,y,len(y)
			lengths.append(y)
		
		filtered_nums[language] = lengths
		
	fp = file('lengths.pkl','wb')
	pickle.dump(filtered_nums,fp)
	fp.close()
	
#get_lengths()
	
fp = file('lengths.pkl','r')
nums = pickle.load(fp)

wrapper = '<a href = "http://omniglot.com/language/numbers/%s.htm"> %s</a> %s <br>'

languages = nums.keys()
languages.sort()
for x in languages[:]:
	try:
		print wrapper%(x,x, str( chain(digits = nums[x]) ) )
	except:
		print ': failed '
		continue
