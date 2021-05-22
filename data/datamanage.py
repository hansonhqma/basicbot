import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from spellchecker import SpellChecker
import string
import os.path
import time
  

def runtime(address):
	browser = webdriver.Chrome("/Applications/code/basicbot/data/chromedriver")
	browser.get(address)
	while True:
		try:
			print("Extending comment section...")
			button = browser.find_element(By.CLASS_NAME, "Igw0E.IwRSH.YBx95._4EzTm.NUiEW")
			time.sleep(0.75)
			button.click()
		except:
			break

	source = browser.page_source
	data = BeautifulSoup(source, 'html.parser')
	blocks = []
	commentsections = data.findAll('ul', attrs={'class':'Mr508'})
	print("Scraping comments...")
	for commentblock in commentsections:
		block = commentblock.find('div', attrs={'class':'C4VMK'})
		text = block.find('span').text
		if "@" not in text and not text == "Verified" and "#" not in text:
			blocks.append(text)
	browser.close()
	browser.quit()
	return blocks

def buildraw(): #removes all emojis from text
	spell = SpellChecker()
	legal = string.printable
	comments = open("comments.txt")
	towrite = open("comments_raw.txt", "r+")
	towrite.truncate(0)

	while True:
		line = list(comments.readline().strip())
		if line == []:
			break
		illegal = list(set(line).difference(set(legal)))

		for character in illegal:
			while character in line:
				index = line.index(character)
				line.pop(index)
		while '.' in line:
			index = line.index('.')
			line.pop(index)
		line = ("".join(line)).lower()
		line = line.split(" ")
		for i in range(len(line)):
			line[i] = spell.correction(line[i])
		line = " ".join(line)
		line = line.strip() + ";"
		if len(line) > 1:
			towrite.write(line+"\n")

	towrite.close()
	comments.close()

def add_to_data(rawtext):
	comments = open("comments.txt", 'a')
	comments.write(rawtext+"\n")
	comments.close()
	buildraw()

def scrape():
	textfile = open("comments.txt", 'a')
	while True:
		userin = input("Enter Address: ")
		if userin.lower() == "stop":
			break
		text = runtime(userin)
		for line in text:
			textfile.write(line+'\n')
		print("Comments added.")
	textfile.close()
	buildraw()

