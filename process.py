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

def build_weighted_selections(chain, selectionlist):
	weighted_selection_list = []
	end_cases = 0
	end_keys = []
	for item in selectionlist:
		if item[-1] == ";":
			end_keys.append(item)
			end_cases += 1
			continue
		child_count = len(chain[item])
		for i in range(child_count):
			weighted_selection_list += [item]
	end_case_probablity = end_cases/len(selectionlist)

	if end_case_probablity == 1:
		return end_keys

	elif end_cases > 0:
		inflate = int(len(weighted_selection_list)/(1-float(end_case_probablity)))-len(weighted_selection_list)
		inflate_per_case = inflate//end_cases
		for item in end_keys:
			for i in range(inflate_per_case):
				weighted_selection_list.append(item)

	return weighted_selection_list


def serve_comment(markovdictionary):
	weighted_list = build_weighted_selections(markovdictionary, list(markovdictionary.keys()))
	output = [random.choice(weighted_list)]
	initwords = list(markovdictionary.keys())

	while True:
		key = output[-1]
		selections = build_weighted_selections(markovdictionary, list(markovdictionary[key]))
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
		print("Pruned MDT:-----\t", serve_comment(prunedchain))
		print("Unpruned MDT:---\t", serve_comment(chain))
