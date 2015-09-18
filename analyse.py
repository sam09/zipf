from __future__ import print_function
import collections,keyword,tokenize,sys,matplotlib
from matplotlib import pyplot as plt
from operator import itemgetter
import numpy as np
import requests
import io
from bs4 import BeautifulSoup

font = {'family' : 'sans-serif', 'weight' : 'normal', 'size' : 12}
matplotlib.rc('font', **font)
fig = plt.figure(figsize = (15,15))
tokenCounter = collections.Counter(keyword.kwlist)
maxLinks = 500

for word in keyword.kwlist:
	tokenCounter[word] = tokenCounter[word] - 1
	
def countKeywords():
	processedKeywords = 0
	processedLinks = 0
	with open('links.txt') as links:
		for link in links:
			try:
				htmlFile = requests.get(link.rstrip()).text
				with io.StringIO(htmlFile) as fileReader:
					tokens = (token for _, token, _, _, _ in tokenize.generate_tokens(fileReader.readline))
					for token in tokens:
						if keyword.iskeyword(token):
							processedKeywords = processedKeywords + 1
							tokenCounter[token] = tokenCounter[token] + 1
				processedLinks += 1
				if processedLinks > maxLinks:
					break
				progressString = "\rProcessed {0} links and {1} keywords".format(processedLinks,processedKeywords)
				print(progressString,end = '')
			except:
				pass
	return sorted(tokenCounter.items(),key = itemgetter(1),reverse = True)


def plotBarGraph(tokenCounts):
	tokenCounts = zip(*tokenCounts)
	numElements = np.arange(len(tokenCounts[0]))
	thickness = 0.45
	topOffset = max(tokenCounts[1]) + len(str(max(tokenCounts[1])))
	plt.ylim([0,topOffset])
	plt.xlim([-1,len(tokenCounts[0])])
	plt.xticks(numElements,tokenCounts[0],rotation = 55, verticalalignment = 'top')
	rects = plt.bar(numElements,tokenCounts[1], width = thickness, linewidth = 1.5, edgecolor = 'black', color = 'green', align = 'center')
	for rect,count in zip(rects,tokenCounts[1]):
		height = rect.get_height()
		plt.text(rect.get_x()+rect.get_width()/2., 1.01*height, '%d'% count,
			ha='center', va='bottom')
	plt.show()
			
def main():
	tokenCounts = countKeywords()
	plotBarGraph(tokenCounts)
	
if __name__ == '__main__':
	main()