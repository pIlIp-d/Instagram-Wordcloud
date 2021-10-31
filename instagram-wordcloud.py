#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ==================================================================
#   Instagram Wordcloud -- a tool for category visualization  
#
#   Copyright 2021 Philip Dell
#   MIT License
#
#   Source Repository: https://github.com/pIlIp-d/Instagram-wordcloud
# ==================================================================

#time
from datetime import datetime
dt = datetime.now()
time = datetime.timestamp(dt)

###init
import csv, sys, os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from os.path import exists

import crunch

save = True # change to false if you just want to display the wordcloud

### reading and formating words
print("Instagram Wordcloud")
wordlist = ""

files = []
if exists("ads_interests.html"):
	files.append("ads_interests.html")
else:
	print("[!] ads_interests.html not found.")
if exists("your_topics.html"):
	files.append("your_topics.html")
else:
	print("[!] your_topics.html not found.")
#formating
for file in files:
	print("reading "+file)
	htmldoc = open(file).read()
	soup = BeautifulSoup(htmldoc, "html.parser")
	tag = soup.find_all(class_="_23bw")
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

if wordlist == "":
	print("[!] No words found!")
	quit()
### Generate a word cloud image
print("generating wordcloud\n. . .")
wordcloud = WordCloud(font_path="fonts/PathwayExtreme.ttf", width=3200, height=1600, max_words=600, min_word_length=2, scale = 2).generate(wordlist)#colormap scale
plt.figure( figsize=(20,10), facecolor='k')
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")

### save or show wordcloud
path_exists = False
filenum = 1
while not path_exists:
	if exists("interests_wordcloud_"+str(filenum)+".png"):
		filenum += 1
	else:
		path = "interests_wordcloud_"+str(filenum)+".png"
		path_exists = True
if (save):
	wordcloud.to_file(path)
	#plt.savefig(path)
	print("--wordcloud saved--")
else:
	print("--showing wordcloud--")
	plt.show()


#compression
print("--Compressing via Crunch--")	
crunch.crunch(path)
#replace with compressed file
compressed = "interests_wordcloud_"+str(filenum)+"-crunch.png"
os.remove(path)
os.rename(compressed, path)

##time
dt = datetime.now()
print("\nProcess finished in "+str(datetime.timestamp(dt) - time)[0:5] + "seconds.")

print("\n--programm closed--")
