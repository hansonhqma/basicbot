import random
import nltk

def buildmarkov():
	data = []
	markov = dict()
	file = open("data/comments_raw.txt")
	while True:
		line = file.readline().strip().lower()
		if line == "":
			break
		line = line.split(" ")
		while "" in line:
			index = line.index("")
			line.pop(index)
		data += line


	#built list "data" of words with EOW cases

	for word in data:
		if word[-1] == ";":
			continue

		if word in list(markov.keys()):
			continue

		indices = [i for i, x in enumerate(data) if x == word]
		nexts = []
		for index in indices:
			nexts.append(data[index+1])

		markov[word] = nexts


	return markov


def buildmarkovfromnltk(): #unused at the moment
	nlktmarkov = dict()
	raw_text = ""
	file = open("data/comments_raw.txt")
	while True:
		line = file.readline().strip()
		if line == "":
			break
		line = line.replace(";", "")
		raw_text += str(line + " ")

	tokens = nltk.word_tokenize(raw_text)
	textobject = nltk.Text(tokens)
	generation = str(textobject.generate()).replace("\n", "; ").split(" ")
	generation[-1] += ";"
	
	for word in generation:
		if word[-1] == ";":
			continue

		if word in list(nlktmarkov.keys()):
			continue

		indices = [i for i, x in enumerate(generation) if x == word]
		nexts = []
		for index in indices:
			nexts.append(generation[index+1])

		nlktmarkov[word] = nexts
	return nlktmarkov


def servecomment(markovdictionary):
	output = [random.choice(list(markovdictionary.keys()))]
	
	while True:
		selections = list(markovdictionary[output[-1]])
		word = random.choice(selections)
		output.append(word)
		if word[-1] == ";":
			break

	comment = " ".join(output)

	return comment


if __name__ == "__main__":
	chain = buildmarkov()
	print("Markov chain generated, serving...")
	while True:
		userin = input(">>>> ")
		if userin.lower() == "stop":
			break
		print("\t\t",servecomment(chain))
