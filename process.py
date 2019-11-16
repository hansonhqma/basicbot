import random

def prune_markov_chain(chaindictionary):
	initwords = list(chaindictionary.keys())
	post = list(chaindictionary.values())
	for i in range(len(initwords)):
		keysize = len(chaindictionary[initwords[i]])
		if keysize == 1:
			del chaindictionary[initwords[i]]

	return chaindictionary

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

	#build pruned chain
	pruned = markov.copy()
	pruned = prune_markov_chain(pruned)

	return markov, pruned

def analyzechain(markovchain):
	lengthlist = []
	for i in range(len(markovchain)):
		size = len(markovchain[list(markovchain.keys())[i]])
		lengthlist.append(size)
	maxval, maxindex = max(lengthlist), lengthlist.index(max(lengthlist))
	minval, minindex = min(lengthlist), lengthlist.index(min(lengthlist))
	maxunique, minunique = len(set(list(markovchain.values())[maxindex])), len(set(list(markovchain.values())[minindex]))


	print("\n"+"="*20+" MARKOV CHAIN ANALYTICS "+"="*20+"\n")
	print("--- {} unique initializer nodes\n".format(len(markovchain)))
	print("--- '{}' has the largest branching factor, with {} child nodes and {} unique child nodes\n".format(list(markovchain.keys())[maxindex], maxval, maxunique))
	print("--- '{}' has the smallest branching factor, with {} child notes and {} unique child nodes\n".format(list(markovchain.keys())[minindex], minval, minunique))

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
	chain, prunedchain = buildmarkov()
	print("Markov chains generated - Analytics:")
	analyzechain(chain)
	analyzechain(prunedchain)
	print("="*64)
	print("\nPress enter to generate, type stop and enter to stop\n")
	while True:
		userin = input(": ")
		if userin.lower() == "stop":
			break
		print("\t\t",servecomment(chain))
