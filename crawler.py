import numpy             as np
import networkx          as nx
import matplotlib.pyplot as plt
import pickle
import requests
import re
from pattern import web

class Crawler():
	def __init__(self, startURL, matchURL, n=None):
		self.startURL  = startURL
		self.regex     = matchURL
		self.G         = nx.DiGraph()
		self.nPages    = n
		self.crawled   = list()
		self.crawling  = [startURL,] 
		self.currentId = 0
		return

	def getLinks(self, url):
		'''Returns a list of links contained in the DOM of the page at a given URL'''
		data  = requests.get(url).text
		dom   = web.Element(data)
		links = list()
		for a in dom.by_tag('a'):
			if 'href' in a.attributes:
				links.append(a.attributes['href'].encode('ascii','xmlcharrefreplace'))
		return links

	def cleanLinks(self, dirtyList, currentURL):
		'''Removes url not matching given domain and transform relative paths to absolute paths'''
		cleanList = list()
		for link in dirtyList:
			url = None
			# print 'In:', link
			if self.regex in link:
				if link[:7] == 'http://':
					url = link
				elif link[:2] == '//':
					url = 'http:' + link
			elif len(link) > 0 and link[0] == '/':
				url = self.startURL + link
			if url not in cleanList and url != None:
				cleanList.append(url)
			# print 'Out:', cleanList[-1]
		return cleanList

	def updateNetwork(self, G, url, linksList):
		'''Add fetched links to digraph G'''
		edgesList = [(url, l) for l in linksList]
		G.add_node(url)
		G.add_nodes_from(linksList)
		G.add_edges_from(edgesList)
		return G

	def reloadFromExistingState(self, graph, crawled, crawling, dump=None):
		'''Relaunch from existing dumped state'''
		self.crawled   = self.loadFromFile(crawled)
		self.crawling  = self.loadFromFile(crawling)
		self.G         = nx.read_gml(graph)
		self.currentId = len(self.crawled)
		self.crawl(dump=dump)
		return

	def dumpGraph(self):
		'''Dump graph as a GML file and save png of the network'''
		# Save Graph
		nx.write_gml(self.G, 'graph_full.gml')
		# Plot Graph
		pos = nx.spring_layout(self.G)
		nx.draw_networkx_nodes(self.G, pos, cmap=plt.get_cmap('jet'))
		nx.draw_networkx_edges(self.G, pos, edge_color='k', arrows=True)
		plt.savefig("graph.png", bbox_inches="tight")
		print 'Crawled %d pages, %d remaining' % (len(self.crawled), len(self.crawling))

	def dumpToFile(self, data, fname):
		'''Use pickle to dump data in fname file'''
		f = open(fname, 'w')
		pickle.dump(data, f)
		f.close()
		return

	def loadFromFile(self, fname):
		'''Use pickle to load data from fname file and return it'''
		f    = open(fname, 'r')
		data = pickle.load(f)
		f.close()
		return data

	def crawl(self, n=None, dump=None):
		'''Launch crawler on n pages if n != None, otherwise, it stops when all webpages have been explored'''
		if n != None:
			self.nPages = n
		
		print "Start crawling ", self.startURL

		while (self.nPages == None and len(self.crawling) > 0) or (self.nPages != None and len(self.crawled) <= self.nPages):
			self.currentId += 1
			if dump != None and (self.currentId)%dump == 0:
				# Dump intermediary graph in case of crash or interrupt
				nx.write_gml(self.G, 'graph_%06d.gml' % self.currentId)
				self.dumpToFile(self.crawled,  'crawled_%06d.p' % self.currentId)
				self.dumpToFile(self.crawling, 'crawling_%06d.p'% self.currentId)
			
			currentURL = self.crawling.pop(0)
			print "Crawling page %d of %d:"%(self.currentId, len(self.crawling + self.crawled)), currentURL.encode('ascii','xmlcharrefreplace')
			self.crawled.append(currentURL)
			
			# Get a list of new links from the current page
			dirtyLinks     = self.getLinks(currentURL)
			cleanLinks     = self.cleanLinks(dirtyLinks, currentURL)
			newLinks       = list(set(cleanLinks) - set(self.crawling + self.crawled))
			self.crawling += newLinks
			print '%d of %d new links found on the current page'%(len(newLinks), len(cleanLinks))

			# Build network
			self.G = self.updateNetwork(self.G, currentURL, cleanLinks)
		self.dumpGraph()
		return
		
if __name__ == "__main__":
	bug = Crawler("http://cdiscount.com", "cdiscount.com")
	bug.crawl(n=None, dump=200)