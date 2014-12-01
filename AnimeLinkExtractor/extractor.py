#!/usr/bin/python3

import urllib.request
import re
import tkinter as tk

def extractLinks(animeLink):
	"""Extracts direct links
	
	Extracts direct links to movie from GoGoAnime.com.
	Takes movie link as argument.
	Returns list of direct links.
	"""
	USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.154 Safari/537.36"

	r = urllib.request.Request(animeLink, headers={'User-Agent': USER_AGENT, 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'})
	data = urllib.request.urlopen(r)
	data = data.read()
	frames = re.findall('<p><iframe.*</iframe></p>', str(data))
	frames = re.split('"', str(frames))
	links = []
	for text in frames:
		if text[0:4] == 'http':
			text = re.sub(r'&#038;', "&", text) 
			links.append(text)
	links2 = []
	for link in links:
		r = urllib.request.Request(link, headers={'User-Agent': USER_AGENT})
		data = urllib.request.urlopen(r)
		data = data.read()
		frames = re.findall('_url = ".*";', str(data))
		frames = re.split('"', str(frames))
		for frame in frames:
			if frame[0:4] == 'http':
				links2.append( urllib.parse.unquote(frame) )
	return links2
	
	
class gui:
	def __init__(self, root):
		self.mirrors = []
		self.label = tk.Label(root, text="Script works only with links from GoGoAnime.com\n\nInsert anime link below\n")
		self.label.grid(row=0, columnspan=2)
		
		self.linkE = tk.Entry(root, width=100)
		self.linkE.grid(row=1, column=1)
		self.linkE.delete(0, tk.END)
		
		self.applyB = tk.Button(root, text="Find links", command=self.giveLink)
		self.applyB.grid(row=1, sticky=tk.W)
	def giveLink(self):
		self.links = extractLinks(self.linkE.get())
		for i in self.mirrors:
			i.destroy()
		self.mirrors = []
		for index, link in enumerate(self.links):
			self.mirrors.append( tk.Entry(root, width=110) )
			self.mirrors[index].delete(0, tk.END)
			self.mirrors[index].insert(0, link)
			self.mirrors[index].grid(columnspan=2, sticky=tk.S+tk.W)
		
root = tk.Tk()
root.wm_title("Anime Direct Links Extractor")
app = gui(root)
root.mainloop()
		
		
		
		