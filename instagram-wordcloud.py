#by Philip Dell, MIT-Licence, v2 19.10.2021

###init
import csv, sys
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

save = True # change to false if you just want to display the wordcloud

### reading and formating words
print("reading categories\n")
htmldoc = open("ads_interests.html").read()
soup = BeautifulSoup(htmldoc, "html.parser")
tag = soup.find_all(class_="_23bw")
wordlist = ""
if tag == []:
	print("error: found no categories in html, check if the categories are in html-class called '_23bw'")
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

### Generate a word cloud image
print("generating wordcloud\n. . .")
wordcloud = WordCloud().generate(wordlist)
wordcloud = WordCloud(width=1600, height=800).generate(wordlist)
plt.figure( figsize=(20,10), facecolor='k')
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")


### save or show wordcloud
if (save):
	plt.savefig("interests_wordcloud.png")
	print("--wordcloud saved--")
else:
	print("--showing wordcloud--")
	plt.show()
	
print("--programm closed--")
