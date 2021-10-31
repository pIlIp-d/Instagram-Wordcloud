# -*- coding: utf-8 -*-
# ==================================================================
#   Instagram Wordcloud -- a tool for category visualization  
#
#   Copyright 2021 Philip Dell
#   MIT License
#
#   Source Repository: https://github.com/pIlIp-d/Instagram-wordcloud
# ==================================================================

### options
MAX_WORDS = 600
compress = True

#colors
BACKGROUND = "black"
COLORSCHEME = "cividis" #https://matplotlib.org/stable/gallery/color/colormap_reference.html

'''
wordcloud uses a random factor for fitting in the words
-> little changes in the positioning even when the words are the same

use any combination of colors to create a unique style 
Here are some examples:
______________________

Background - black

	#settled colors -- viridis
	#settled colos -- cividis

	#blue style -- winter
	#light orange style -- Wistia
	#dark orange -- autumn
______________________

Background -- white

	#modern -- inferno
	#brown -- copper
	#light blue, pink -- cool
______________________

Tip for trying different styles - turn off compression
______________________

'''

#time
from datetime import datetime
dt = datetime.now()
time = datetime.timestamp(dt)

###imports
import csv, sys, os
from wordcloud import WordCloud
from os.path import exists
from bs4 import BeautifulSoup
import crunch

def read_files():
	files = []
	if exists("ads_interests.html"): files.append("ads_interests.html")
	else: print("[!] ads_interests.html not found.")
	if exists("your_topics.html"): files.append("your_topics.html")
	else: print("[!] your_topics.html not found.")
	return files

def format(files):	
	wordlist = ""
	for file in files:
		print("reading "+file)
		htmldoc = open(file).read()
		tag = BeautifulSoup(htmldoc, "html.parser").find_all(class_="_23bw")
		if tag == []:
			print("[!] found no categories in html, check if the categories are in html-class called '_23bw'")
			quit()
		for i in tag:
			st = i.string
			st = st.replace("  "," ")
			st = st.replace("(","")
			st = st.replace("\n","")
			st = st.replace("[beta]","")
			st = st.replace("(","")
			st = st.replace(")","")
			st = st.replace(";","")
			st = st.replace(".","")
			st = st.replace("&"," ")
			st = st.replace("-"," ")
			wordlist += st + ","
	return wordlist

def create_wordcloud(wordlist, path):
	print("generating wordcloud\n. . .")
	WordCloud(
		font_path="fonts/PathwayExtreme.ttf", 
		width=3200, height=1600, max_words=MAX_WORDS, min_word_length=2, scale = 2,
		colormap=COLORSCHEME, background_color=BACKGROUND
	).generate(wordlist).to_file(path)
	print("--wordcloud saved--")

def get_path():
	### save or show wordcloud
	filenum = 1
	while True:
		if not exists("interests_wordcloud_"+str(filenum)+".png"):
			return "interests_wordcloud_"+str(filenum)+".png", filenum
		else: filenum += 1

def compresser(path,filenum):
	print("--Compressing via Crunch--")
	compressed = "interests_wordcloud_"+str(filenum)+"-crunch.png"
	path = "interests_wordcloud_"+str(filenum)+".png"
	crunch.crunch(path)
	#replace with compressed file
	os.remove(path)
	os.rename(compressed, path)

def __main__():
	print("Instagram Wordcloud")
	files = read_files()
	wordlist = format(files)
	if wordlist == "":
		print("[!] No words found!")
		quit()

	path, filenum = get_path()
	create_wordcloud(wordlist, path)

	if not os.name == 'nt' and compress:#compression doesnt work on windows
		compresser(path,filenum)

	dt = datetime.now()
	print("\nProcess finished in "+str(datetime.timestamp(dt) - time)[0:5] + " seconds.")
	print("\n--programm closed--")
__main__()
