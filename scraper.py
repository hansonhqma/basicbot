import requests 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
  

def runtime(address):
	browser = webdriver.Chrome('/Applications/code/genthot/chromedriver')
	browser.get(address)
	while True:
		try:
			print("Extending comment section...")
			button = browser.find_element(By.CLASS_NAME, "Igw0E.IwRSH.YBx95._4EzTm.NUiEW")
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
		if "@" not in text and not text == "Verified":
			blocks.append(text)
	browser.close()
	browser.quit()
	return blocks

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