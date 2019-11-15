import string
import nltk

def buildraw(): #removes all emojis from text
	legal = string.printable
	comments = open("comments.txt")
	towrite = open("comments_raw.txt", "a")

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

		line = "".join(line)
		line = line.strip() + ";"
		if len(line) > 1:
			towrite.write(line+"\n")

	towrite.close()