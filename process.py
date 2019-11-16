import random

def chain_safe_remove(chain, key):
	del chain[key]
	keys = list(chain.keys())
	for key2 in keys:
		values = chain[key2]
		if key in values:
			chain[key2].remove(key)

def prune_markov_chain(chaindictionary):
	
	for i in range(2):
		removed = []
		keys = list(chaindictionary.keys())
		for key in keys:
			values = chaindictionary[key]
			if len(values) == i:
				removed.append(key)
		
		for word in removed:
			chain_safe_remove(chaindictionary, word)
	

	return chaindictionary

def build_markov():
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

	return lengthlist


def servecomment(markovdictionary):
	output = [random.choice(list(markovdictionary.keys()))]
	initwords = list(markovdictionary.keys())

	while True:
		key = output[-1]
		selections = list(markovdictionary[key])
		word = random.choice(selections)
		output.append(word)
		if word[-1] == ";":
			break

	comment = " ".join(output)

	return comment


if __name__ == "__main__":
	chain = build_markov()
	prunedchain = prune_markov_chain(build_markov())
	print("Markov chains generated - Analytics:")
	unprunedll = analyzechain(chain)
	prunedll = analyzechain(prunedchain)
	print("="*64)
	print("\nPress enter to generate, type stop and enter to stop\n")
	while True:
		userin = input(": ")
		if userin.lower() == "stop":
			break
		print("Pruned MDT:-----\t", servecomment(prunedchain))
		print("Unpruned MDT:---\t", servecomment(chain))
