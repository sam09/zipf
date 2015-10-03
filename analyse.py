from __future__ import print_function,division
import collections,keyword,tokenize,sys,matplotlib
from matplotlib import pyplot as plt
from operator import itemgetter
import numpy as np
import requests
import io

font = {'family' : 'sans-serif', 'weight' : 'normal', 'size' : 12}
matplotlib.rc('font', **font)
fig1 = plt.figure(figsize = (15,15))
fig2 = plt.figure(figsize = (15,15))
ax1 = fig1.add_subplot(111)
ax2 = fig2.add_subplot(111)
tokenCounter = collections.Counter(keyword.kwlist)
maxLinks = 850

for word in keyword.kwlist:
	tokenCounter[word] = tokenCounter[word] - 1
	
def countKeywords():
	processedKeywords = 0
	with open('dump.py','r') as codeReader:
		tokens = (token for _, token, _, _, _ in tokenize.generate_tokens(codeReader.readline))
		for token in tokens:
			if keyword.iskeyword(token):
				processedKeywords = processedKeywords + 1
				tokenCounter[token] = tokenCounter[token] + 1
		progressString = "\rProcessed {0} keywords".format(processedKeywords)
		print(progressString,end = '')
	return sorted(tokenCounter.items(),key = itemgetter(1),reverse = True)
	
def getLotsOfCode():
	processedLinks = 0
	with open('links.txt') as links, open('dump.py','a') as codeFile:
		for link in links:
			try:
				if processedLinks > maxLinks:
					break
				htmlFile = requests.get(link.rstrip()).text
				with io.StringIO(htmlFile) as fileReader:
					for line in fileReader.readlines():
						codeFile.write(line)
				processedLinks += 1
				progressString = "\rProcessed {0} links".format(processedLinks)
				print(progressString,end = '')
			except:
				pass
	return sorted(tokenCounter.items(),key = itemgetter(1),reverse = True)

def getHarmonicSum(N,S):
	array = np.arange(1,N+1,dtype = float)
	harmonicSum = 0
	for element in array:
		harmonicSum += (1/(element**S))
	return harmonicSum
	
def getIdealFrequency(K,S):
	harmonicSum = getHarmonicSum(K,S)
	array = np.arange(1,K+1,dtype = float)
	for index in xrange(K):
		array[index] = harmonicSum/24*(1/(array[index]**S))
	return array
	
def plotBarGraph(tokenCounts):
	tokenCounts = zip(*tokenCounts)
	numElements = np.arange(len(tokenCounts[0]))
	thickness = 0.45
	topOffset = max(tokenCounts[1]) + len(str(max(tokenCounts[1])))
	ax1.set_title('Keywords vs Occurnces')
	ax1.set_xlabel('Keywords')
	ax1.set_ylabel('Occurences')
	ax1.xaxis.set_label_coords(1.05, 0.015)
	ax1.set_xticks(numElements)
	ax1.set_xticklabels(tokenCounts[0],rotation = 55, verticalalignment = 'top')
	ax1.set_ylim([0,topOffset])
	ax1.set_xlim([-1,len(tokenCounts[0])])
	rects = ax1.bar(numElements,tokenCounts[1], width = thickness, linewidth = 1.5, edgecolor = 'black', color = 'green', align = 'center')
	for rect,count in zip(rects,tokenCounts[1]):
		height = rect.get_height()
		ax1.text(rect.get_x()+rect.get_width()/2., 1.01*height, '%d'% count,
			ha='center', va='bottom')

def plotLog(tokenCounts):
	tokenCounts = zip(*tokenCounts)
	numElements = np.arange(31)
	idealCurve = getIdealFrequency(31,0.2)
	ax2.set_title('Keywords vs Occurnces')
	ax2.set_xlabel('Log(Rank)')
	ax2.set_ylabel('Log(Frequency)')
	ax2.set_xticks(numElements)
	ax2.set_xticklabels(tokenCounts[0], verticalalignment = 'top')
	ax2.loglog(numElements,idealCurve,basex = 10,basey = 10)
	frequencies = list(tokenCounts[1])
	maxFreq = max(frequencies)
	for index in xrange(len(frequencies)):
		frequencies[index] /= maxFreq
	ax2.loglog(numElements,frequencies,basex = 10,basey = 10)
			
def main():
	tokenCounts = countKeywords()
	plotBarGraph(tokenCounts)
	plotLog(tokenCounts)
	plt.show()
	#getLotsOfCode()
	
if __name__ == '__main__':
	main()